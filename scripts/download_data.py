import pandas as pd
import yfinance as yf
from quantlab.data import REQUIRED_COLUMNS, validate_ohlcv
from pathlib import Path

TICKERS = ["SPY", "QQQ", "GLD", "BTC-USD"]
START_DATE = "2021-01-01"
END_DATE = "2026-01-01"
OUTPUT_DIR = Path("data")

def download_market_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Download daily historical market data for a single asset.
    """
    df = yf.download(tickers=ticker, start=start, end=end, interval="1d", auto_adjust=False, multi_level_index=False, progress=False)
    if df is None or df.empty:
        raise ValueError(f"No market data downloaded for ticker '{ticker}'.")
    return df

def normalize_yfinance_data(frame: pd.DataFrame) -> pd.DataFrame:
    """
    Convert Yahoo Finance market data to the QuantLab OHLCV schema.
    """
    normalized = frame.copy().reset_index()

    column_mapping = {
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
    }

    normalized = normalized.rename(columns=column_mapping)
    if "date" in normalized.columns:
        normalized["date"] = pd.to_datetime(normalized["date"]).dt.strftime("%Y-%m-%d")

    missing = [col for col in REQUIRED_COLUMNS if col not in normalized.columns]
    if missing:
        raise ValueError(f"Missing expected normalized columns: {', '.join(missing)}")

    return normalized[REQUIRED_COLUMNS]

def save_market_data(ticker: str, frame: pd.DataFrame, output_dir: Path) -> Path:
    """
    Validate and save historical market data to a CSV file.
    """
    validated = validate_ohlcv(frame)
    output_dir.mkdir(parents=True, exist_ok=True)
    file = output_dir / f"{ticker}.csv"
    validated.to_csv(file, index=True, date_format="%Y-%m-%d")
    return file


def main() -> None:
    """
    Download, normalize, validate, and save historical market data for all tickers.
    """
    for ticker in TICKERS:
        raw_data = download_market_data(ticker, START_DATE, END_DATE)
        normalized_data = normalize_yfinance_data(raw_data)
        output_path = save_market_data(ticker, normalized_data, OUTPUT_DIR)
        print(f"[OK] {ticker:<7} | {len(normalized_data):>4} observations | {output_path}")


if __name__ == "__main__":
    main()