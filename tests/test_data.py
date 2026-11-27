import pandas as pd
import pytest
from io import StringIO
from quantlab.data import adjust_ohlc, load_csv, validate_ohlcv
import numpy as np 

def test_load_csv_valid_file():

    path = "tests/fixtures/sample_ohlcv.csv"
    df = load_csv(path)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (65,6)
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index[0] == pd.Timestamp("2025-01-06")
    assert df["close"].iloc[0] == 102.0
    assert df["close"].iloc[-1] == 124.4
    assert df.columns.tolist() == ["open", "high", "low", "close", "adj_close", "volume"]


def test_load_csv_missing_file(tmp_path):
    missing_path = tmp_path / "nonexistent_test_file.csv"
    with pytest.raises(FileNotFoundError) :
        load_csv(missing_path)

def test_load_csv_from_buffer(): 
    data = "date,open,high,low,close,adj_close,volume\n2025-01-06,100,105,98,102,102,150000\n2025-01-07,102,108,101,106,106,180000"
    df = load_csv(StringIO(data))

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 6)
    assert df["open"].iloc[0] == 100.0
    assert df["close"].iloc[-1] == 106.0
    assert df["volume"].iloc[-1] == 180000
    assert isinstance(df.index, pd.DatetimeIndex)
    assert (df.dtypes == "float64").all()

@pytest.fixture
def raw_ohlcv():

    data = {
        "date": ["2025-01-06", "2025-01-07", "2025-01-08"],
        "open": [100, 102, 106],
        "high": [105, 108, 110],
        "low": [98, 101, 104],
        "close": [102, 106, 108],
        "adj_close": [102, 106, 108],
        "volume": [150000, 180000, 200000],
    }

    df = pd.DataFrame(data)

    return df

def test_validate_ohlcv_valid_data(raw_ohlcv):

    df = validate_ohlcv(raw_ohlcv)

    assert df.shape == (3, 6)
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.name == "date"
    assert (df.dtypes == "float64").all()
    assert df.index.is_monotonic_increasing
    assert df["close"].iloc[0] == 102.0
    assert df["close"].iloc[-1] == 108.0


def test_validate_ohlcv_missing_columns(raw_ohlcv):
    df = raw_ohlcv.drop(columns=["high", "volume"])
    with pytest.raises(ValueError, match="Missing required columns: high, volume"):
        validate_ohlcv(df)


def test_validate_ohlcv_empty_data(raw_ohlcv):
    empty_df = raw_ohlcv.iloc[0:0]
    with pytest.raises(ValueError, match="Empty dataset"):
        validate_ohlcv(empty_df)

@pytest.mark.parametrize("invalid_date", ["2025-02-30", "hello", "2025-13-01", "2025-1-6", "2025-01-06 12:30:00" , None])
def test_validate_ohlcv_invalid_date(raw_ohlcv, invalid_date):
    raw_ohlcv.loc[0, "date"] = invalid_date
    with pytest.raises(ValueError, match="Invalid date found in 'date' column."):
        validate_ohlcv(raw_ohlcv)


def test_validate_ohlcv_duplicate_dates(raw_ohlcv):
    raw_ohlcv.loc[1, "date"] = "2025-01-06" 
    with pytest.raises(ValueError, match="Duplicate dates found in 'date' column."):
        validate_ohlcv(raw_ohlcv)


def test_validate_ohlcv_sorts_dates(raw_ohlcv):
    df = validate_ohlcv(raw_ohlcv.iloc[::-1])

    assert df.index.is_monotonic_increasing
    assert df.index[0] == pd.Timestamp("2025-01-06")
    assert df["close"].tolist() == [102.0, 106.0, 108.0]


@pytest.mark.parametrize(
    "column, value, expected_error",
    [
        ("low", -10, "Prices must be strictly positive"),
        ("low", 0, "Prices must be strictly positive"),
        ("close", np.nan, "Missing values found in price columns"),
        ("adj_close", np.inf, "Prices must be finite"),
        ("open", -np.inf, "Prices must be finite"),
        ("open", "hello", "Invalid numerical data"),
    ],
)
def test_validate_ohlcv_invalid_price(raw_ohlcv, column, value, expected_error):
    raw_ohlcv[column] = raw_ohlcv[column].astype(object)
    raw_ohlcv.loc[0, column] = value
    with pytest.raises(ValueError, match=expected_error):
        validate_ohlcv(raw_ohlcv)

@pytest.mark.parametrize(
    "value, expected_error",
    [
        (-100, "Negative values found"),
        (np.inf, "Volume must be finite"),
        (-np.inf, "Volume must be finite"),
        ("hello", "Invalid numerical data"),
    ],
)
def test_validate_ohlcv_invalid_volume(raw_ohlcv, value, expected_error):
    raw_ohlcv["volume"] = raw_ohlcv["volume"].astype(object)
    raw_ohlcv.loc[0, "volume"] = value
    with pytest.raises(ValueError, match=expected_error):
        validate_ohlcv(raw_ohlcv)

@pytest.mark.parametrize("valid_volume", [0, np.nan, 150000])
def test_validate_ohlcv_valid_volume(raw_ohlcv, valid_volume):
    raw_ohlcv["volume"] = raw_ohlcv["volume"].astype(object)
    raw_ohlcv.loc[0, "volume"] = valid_volume

    df = validate_ohlcv(raw_ohlcv)
    actual = df["volume"].iloc[0]

    if pd.isna(valid_volume):
        assert pd.isna(actual)
    else:
        assert actual == valid_volume

@pytest.mark.parametrize(
    "column, value",
    [
        ("high", 101),
        ("open", 106), 
        ("low", 101),
        ("close", 97),
        ("high", 97)
    ],
)
def test_validate_ohlcv_inconsistent_ohlc(raw_ohlcv, column, value):
    raw_ohlcv.loc[0, column] = value
    with pytest.raises(ValueError, match="Inconsistent OHLC values found."):
        validate_ohlcv(raw_ohlcv)

def test_validate_ohlcv_numeric_strings(raw_ohlcv):
    raw_ohlcv["close"] = raw_ohlcv["close"].astype(str)
    df = validate_ohlcv(raw_ohlcv)
    assert df["close"].dtype == "float64"
    assert df["close"].tolist() == [102.0, 106.0, 108.0]

def test_validate_ohlcv_ignores_extra_columns(raw_ohlcv):
    raw_ohlcv["currency"] = "USD"
    result = validate_ohlcv(raw_ohlcv)
    assert result.shape == (3, 6)
    assert "currency" not in result.columns
    assert result.columns.tolist() == ["open", "high", "low", "close", "adj_close", "volume"]

def test_validate_ohlcv_does_not_mutate_input(raw_ohlcv):
    expected = raw_ohlcv.copy(deep=True)
    validate_ohlcv(raw_ohlcv)
    pd.testing.assert_frame_equal(raw_ohlcv, expected)

@pytest.fixture
def validated_ohlcv():
    dates = pd.DatetimeIndex(
        ["2025-01-06", "2025-01-07", "2025-01-08"],
        name="date",
    )
    data = {
        "open": [98, 50, 100],
        "high": [104, 53, 110],
        "low": [96, 49, 90],
        "close": [100, 52, 104],
        "adj_close": [50, 52, 78],
        "volume": [150000, 180000, 200000],
    }
    return pd.DataFrame(data, index=dates, dtype="float64")

def test_adjust_ohlc_no_adjustment(validated_ohlcv):
    validated_ohlcv["adj_close"] = validated_ohlcv["close"]
    expected = validated_ohlcv.copy(deep=True)
    result = adjust_ohlc(validated_ohlcv)
    pd.testing.assert_frame_equal(result, expected, check_exact=True)

expected = np.array(
    [
        [49.0, 52.0, 48.0, 50.0],
        [50.0, 53.0, 49.0, 52.0],
        [75.0, 82.5, 67.5, 78.0],
    ],
    dtype="float64",
)
def test_adjust_ohlc_correct_values(validated_ohlcv):
    result = adjust_ohlc(validated_ohlcv)
    actual = result[["open", "high", "low", "close"]].to_numpy()
    np.testing.assert_allclose(actual, expected, rtol=1e-9, atol=1e-10)

def test_adjust_ohlc_close_consistency(validated_ohlcv):
    result = adjust_ohlc(validated_ohlcv)
    np.testing.assert_allclose(result["close"].to_numpy(), result["adj_close"].to_numpy(), rtol=1e-9, atol=1e-10)

def test_adjust_ohlc_preserves_structure(validated_ohlcv):
    expected = validated_ohlcv.copy(deep=True)
    result = adjust_ohlc(validated_ohlcv)
    assert result["volume"].equals(expected["volume"])
    assert result["adj_close"].equals(expected["adj_close"])
    assert result.index.equals(expected.index)
    assert result.columns.equals(expected.columns)
    assert result.shape == expected.shape

def test_adjust_ohlc_does_not_mutate_input(validated_ohlcv):
    expected = validated_ohlcv.copy(deep=True)
    adjust_ohlc(validated_ohlcv)
    pd.testing.assert_frame_equal(validated_ohlcv, expected, check_exact=True)

def test_load_csv_invalid_data():
    csv_data = (
        "date,open,high,low,close,adj_close,volume\n"
        "2025-01-06,100,90,98,102,102,150000\n"
    )
    with pytest.raises(ValueError, match="Inconsistent OHLC values found."):
        load_csv(StringIO(csv_data))

def test_market_data_pipeline():
    csv_data = (
        "date,open,high,low,close,adj_close,volume\n"
        "2025-01-07,50,53,49,52,52,180000\n"
        "2025-01-06,98,104,96,100,50,150000\n"
    )
    raw = load_csv(StringIO(csv_data))

    assert raw.shape == (2, 6)
    assert isinstance(raw.index, pd.DatetimeIndex)
    assert raw.index.is_monotonic_increasing
    assert raw["close"].iloc[0] == 100.0

    adj = adjust_ohlc(raw)
    expected_ohlc = np.array(
        [
            [49.0, 52.0, 48.0, 50.0],
            [50.0, 53.0, 49.0, 52.0],
        ],
        dtype="float64",
    )
    np.testing.assert_allclose(
        adj[["open", "high", "low", "close"]].to_numpy(),
        expected_ohlc,
        rtol=1e-9,
        atol=1e-10,
    )
    np.testing.assert_allclose(
        adj["volume"].to_numpy(),
        np.array([150000.0, 180000.0], dtype="float64"),
        rtol=1e-9,
        atol=1e-10,
    )