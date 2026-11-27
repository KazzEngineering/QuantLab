import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
]

PRICE_COLUMNS = [
    "open",
    "high",
    "low",
    "close",
    "adj_close",
]

def load_csv(path_or_file) -> pd.DataFrame:
    """
    Load and validate historical financial data from a CSV file.

    Parameters
    ----------
    path_or_file
        Path to the CSV file or a readable file object.

    Returns
    -------
    pd.DataFrame
        Validated market data indexed by date and sorted chronologically.
    """

    df = pd.read_csv(path_or_file)

    return validate_ohlcv(df)


def validate_ohlcv(frame: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and normalize historical OHLCV data.

    Parameters
    ----------
    frame : pd.DataFrame
        Raw financial market data.

    Returns
    -------
    pd.DataFrame
        Validated and chronologically sorted market data.

    Raises
    ------
    ValueError
        If the dataset contains invalid market data.
    """
    copy_df = frame.copy()

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in copy_df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    if copy_df.empty:
        raise ValueError("Empty dataset")

    date_str = copy_df["date"].astype("string")
    valid_format = date_str.str.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", na=False)
    if not valid_format.all():
        raise ValueError("Invalid date found in 'date' column.")

    copy_df["date"] = pd.to_datetime(copy_df["date"], errors="coerce", format="%Y-%m-%d")
    if copy_df["date"].isna().any():
        raise ValueError("Invalid date found in 'date' column.")

    if copy_df["date"].duplicated().any():
        raise ValueError("Duplicate dates found in 'date' column.")
    
    numeric_columns = [col for col in REQUIRED_COLUMNS if col != "date"]

    copy_df = copy_df[REQUIRED_COLUMNS].copy()
    
    for col in numeric_columns:
        was_na = copy_df[col].isna()  
        copy_df[col] = pd.to_numeric(copy_df[col], errors="coerce").astype("float64")  
        if (copy_df[col].isna() & ~was_na).any():  
            raise ValueError("Invalid numerical data.")

    if copy_df[PRICE_COLUMNS].isna().any().any() :
        raise ValueError("Missing values found in price columns.")

    if not np.isfinite(copy_df[PRICE_COLUMNS]).all().all(): 
        raise ValueError("Prices must be finite.")

    if not np.isfinite(copy_df["volume"].dropna()).all(): 
        raise ValueError("Volume must be finite.")
    
    if (copy_df[PRICE_COLUMNS] <= 0).any().any() :
        raise ValueError("Prices must be strictly positive.")

    if (copy_df["volume"] < 0).any():
        raise ValueError("Negative values found in 'volume' column.")

    if((copy_df["high"] < copy_df["low"])
        | (copy_df["high"] < copy_df["open"])
        | (copy_df["high"] < copy_df["close"])
        | (copy_df["low"] > copy_df["open"])
        | (copy_df["low"] > copy_df["close"])).any() :
        raise ValueError("Inconsistent OHLC values found.")

    copy_df = copy_df.set_index("date").sort_index()

    return copy_df

def adjust_ohlc(frame: pd.DataFrame) -> pd.DataFrame:
    """
    Adjust OHLC prices using the adjusted closing price.

    Parameters
    ----------
    frame : pd.DataFrame
        Validated financial market data.

    Returns
    -------
    pd.DataFrame
        Financial market data with adjusted OHLC prices.
    """
    
    copy_df = frame.copy()

    adjustment_factors = copy_df["adj_close"] / copy_df["close"]

    ohlc_columns = [col for col in PRICE_COLUMNS if col != "adj_close"] 

    for col in ohlc_columns:
        copy_df[col] = copy_df[col]*adjustment_factors

    return copy_df