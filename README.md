<div align="center">

# QuantLab

### Quantitative Finance · Software Engineering · Applied Mathematics

A Python and C++ quantitative research laboratory for financial
market analysis, risk measurement, statistical modelling
and numerical computing.

<br/>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-42_passed-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

![Status](https://img.shields.io/badge/Status-In_Development-orange?style=flat-square)
![Data](https://img.shields.io/badge/Market_Data-5591_Observations-blue?style=flat-square)
![Verification](https://img.shields.io/badge/Verification-68_Passed-brightgreen?style=flat-square)

<br/>

[Overview](#overview) ·
[Roadmap](#roadmap) ·
[Market Data](#market-data) ·
[Installation](#installation) ·
[Usage](#usage) ·
[Testing](#testing--validation)

</div>

---

## Overview

QuantLab is a personal engineering project designed to explore
quantitative finance through the development of a modular,
reliable and reproducible Python research laboratory.

The project combines three complementary disciplines:

| Software Engineering | Quantitative Finance | Applied Mathematics |
|:---|:---|:---|
| Modular architecture | Financial markets | Probability |
| Data processing | Asset returns | Statistics |
| Automated testing | Risk measurement | Linear algebra |
| Numerical computing | Trading strategies | Financial modelling |
| Software reliability | Backtesting | Numerical methods |

The objective is to develop a strong understanding of the financial
and mathematical concepts behind quantitative research, while
applying rigorous software engineering practices.

---

## Project Roadmap

| Phase | Description | Status |
|:---:|:---|:---:|
| 0 | Project Setup & Architecture | ✅ Completed |
| 1 | Market Data Engineering | ✅ Completed |
| 2 | Financial Returns & Risk Analytics | ⏳ Planned |
| 3 | Statistical Analysis & Asset Comparison | ⏳ Planned |
| 4 | Technical Indicators | ⏳ Planned |
| 5 | C++ Numerical Computing & Benchmarks | ⏳ Planned |
| 6 | Quantitative Research & Interactive Visualization | ⏳ Planned |
| 7 | Technical Report, CI & Final Release | ⏳ Planned |

**Target release:** v1.0.0 - January 2027

---

## Market Data

QuantLab uses five years of daily historical market data,
covering different asset classes and trading calendars.

| Ticker | Asset | Asset Class | Observations |
|:---|:---|:---|---:|
| `SPY` | S&P 500 ETF | Equity | 1,255 |
| `QQQ` | Nasdaq-100 ETF | Equity | 1,255 |
| `GLD` | Gold ETF | Commodity | 1,255 |
| `BTC-USD` | Bitcoin | Cryptocurrency | 1,826 |
| | **Total** | | **5,591** |

- **Source:** Yahoo Finance via yfinance
- **Period:** January 2021 – December 2025
- **Frequency:** Daily
- **Currency:** USD
- **Download date:** November 27, 2026

Historical market data is excluded from version control
and remains subject to the provider's usage rights.

---

## Project Structure

```text
QuantLab/
├── data/                 # Local historical market data
├── quantlab/
│   ├── __init__.py
│   └── data.py           # Market data processing
├── scripts/
│   ├── download_data.py  # Historical data acquisition
│   └── verify_data.py    # Market data verification
├── tests/
│   ├── fixtures/         # Synthetic financial datasets
│   └── test_data.py      # Automated unit tests
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/KazzEngineering/QuantLab.git
cd QuantLab
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Usage

### Download Market Data

```bash
python -m scripts.download_data
```

### Verify Market Data

```bash
python -m scripts.verify_data
```

### Load and Adjust Financial Data

```python
from quantlab.data import load_csv, adjust_ohlc

data = load_csv("data/SPY.csv")
adjusted_data = adjust_ohlc(data)

print(adjusted_data.head())
```

---

## Testing & Validation

Run the automated test suite:

```bash
python -m pytest -v
```

<div align="center">

| Automated Tests | Verification Checks | Validated Datasets | Observations |
|:---:|:---:|:---:|:---:|
| **42 passed** | **68 passed** | **4** | **5,591** |

</div>

Unit tests use synthetic datasets and can be executed offline.

The market data verification pipeline checks numerical consistency,
data integrity, chronological ordering and financial price adjustments.

---

## Development Philosophy - No AI-Generated Core Code

QuantLab is a hands-on engineering and learning project.

All core quantitative modules are implemented independently,
without AI-generated code.

Every algorithm, mathematical formula and financial concept
is studied, implemented, understood and validated manually.

The objective is not simply to build a working quantitative
library, but to develop genuine engineering and quantitative
finance expertise.

---

<div align="center">

## Author

**KazzEngineering**

Engineering Student  
Software Engineering · Quantitative Finance · Applied Mathematics

[![GitHub](https://img.shields.io/badge/GitHub-KazzEngineering-181717?style=for-the-badge&logo=github)](https://github.com/KazzEngineering)

</div>