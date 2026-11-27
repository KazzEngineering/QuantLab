import numpy as np
import pandas as pd
from pathlib import Path

from quantlab.data import load_csv, adjust_ohlc, PRICE_COLUMNS

DATA_DIR = Path("data")

EXPECTED_DATA = {
    "SPY": (1255, "2021-01-04", "2025-12-31"),
    "QQQ": (1255, "2021-01-04", "2025-12-31"),
    "GLD": (1255, "2021-01-04", "2025-12-31"),
    "BTC-USD": (1826, "2021-01-01", "2025-12-31"),
}


def main() -> None:
    for ticker, (expected_rows, start, end) in EXPECTED_DATA.items():

        df = load_csv(DATA_DIR / f"{ticker}.csv")
        adjusted = adjust_ohlc(df)

        factors = df["adj_close"] / df["close"]

        checks = {
            "Expected dimensions": df.shape == (expected_rows, 6),
            "Datetime index": isinstance(df.index, pd.DatetimeIndex),
            "Unique dates": df.index.is_unique,
            "Sorted dates": df.index.is_monotonic_increasing,
            "Correct first date": df.index.min() == pd.Timestamp(start),
            "Correct last date": df.index.max() == pd.Timestamp(end),
            "Float64 columns": (df.dtypes == "float64").all(),
            "No missing prices": not df[PRICE_COLUMNS].isna().any().any(),
            "Positive prices": (df[PRICE_COLUMNS] > 0).all().all(),
            "Finite prices": np.isfinite(df[PRICE_COLUMNS]).all().all(),
            "Finite adjusted prices": np.isfinite(adjusted[PRICE_COLUMNS]).all().all(),
            "Adjusted close consistency": np.allclose(
                adjusted["close"], adjusted["adj_close"]
            ),
            "Volume unchanged": adjusted["volume"].equals(df["volume"]),
            "Adj close unchanged": adjusted["adj_close"].equals(df["adj_close"]),
            "Shape unchanged": adjusted.shape == df.shape,
            "Index unchanged": adjusted.index.equals(df.index),
            "Columns unchanged": adjusted.columns.equals(df.columns),
        }

        print(f"\n{'=' * 60}")
        print(f"MARKET DATA VERIFICATION — {ticker}")
        print(f"{'=' * 60}")

        print(f"Observations: {len(df)}")
        print(f"First date:   {df.index.min().date()}")
        print(f"Last date:    {df.index.max().date()}")
        print(f"Missing volume: {df['volume'].isna().sum()}")

        print("\nAdjustment factors:")
        print(factors.describe().to_string())

        print("\nValidation checks:")

        for name, passed in checks.items():
            status = "PASS" if passed else "FAIL"
            print(f"[{status}] {name}")

        if not all(checks.values()):
            raise AssertionError(f"Verification failed for {ticker}.")

        print(f"\n[SUCCESS] {ticker} — All {len(checks)} checks passed.")

    print("\n" + "=" * 60)
    print("ALL MARKET DATASETS SUCCESSFULLY VERIFIED")
    print("=" * 60)


if __name__ == "__main__":
    main()