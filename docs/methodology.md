# Analysis & Feature Engineering Methodology

This document outlines the data ingestion, preprocessing, cleaning, and mathematical calculation logic implemented in the Stock Market Dashboard pipeline.

## 1. Data Ingestion & Reshaping
Yahoo Finance (`yfinance`) downloads stock price metrics for multiple tickers in a wide, MultiIndex format:
- Level 0: Metric type (`Open`, `High`, `Low`, `Close`, `Volume`)
- Level 1: Ticker symbol (`AAPL`, `MSFT`, etc.)

To transform this into a relational dataset suitable for database ingestion and visualization, we stack Level 1 (Ticker) from columns to row values, resulting in:
- `Date` (Index)
- `Ticker` (Stacked Level 1 Index)
- Level 0 metrics (Columns)

We reset the index, producing a tidy tabular format where each row represents a unique `(Date, Ticker)` observation.

## 2. Column Mapping Correction
In the legacy implementation, columns were mapped hardcoded by index sequence:
`Date, Open, High, Low, Close, Adj_Close, Volume`
Because pandas stacking results in alphabetical sorting or puts the Ticker index level at index position 1, columns were shifted:
- `Ticker` values were placed under the `Open` column.
- `Close` values were placed under the `High` column.
- `High` values were placed under the `Low` column.
- `Low` values were placed under the `Close` column.
- `Open` values were placed under `Adj_Close`.

Our refactored `data_cleaner.py` uses string-based rename maps:
```python
rename_map = {
    "level_1": "Ticker",
    "Open": "Open",
    "High": "High",
    "Low": "Low",
    "Close": "Close",
    "Volume": "Volume"
}
```
This guarantees that price indicators correspond exactly to their true values.

## 3. Data Validation & Constraints
We enforce constraints:
- `Volume >= 0`
- `Open`, `High`, `Low`, `Close` >= 0
- `High >= Low`

If any row violates these constraints, a warning is logged into `logs/errors.log`.

## 4. Technical Indicators

### Daily Return
Daily returns represent percentage change in the closing price. The original code did:
`df['Daily_Return'] = df['Close'].pct_change() * 100`
Because the stacked rows were sorted by Date, this compared the price of the first ticker (e.g. `AAPL`) to the second (e.g. `AMZN`) on the same day, yielding meaningless values.

We correct this calculation by grouping by Ticker before applying the percentage change:
$$\text{Daily Return}_{t} = \frac{\text{Close}_{t} - \text{Close}_{t-1}}{\text{Close}_{t-1}} \times 100$$
```python
df['Daily_Return'] = df.groupby('Ticker')['Close'].pct_change() * 100
```

### Simple Moving Average (MA_20)
We calculate the 20-day Simple Moving Average on Close price grouped by Ticker:
$$\text{MA\_20}_{t} = \frac{1}{20} \sum_{i=0}^{19} \text{Close}_{t-i}$$
```python
df['MA_20'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=20).mean())
```
