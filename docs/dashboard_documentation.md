# Power BI Dashboard Documentation

This document describes the structure, KPIs, visuals, and configurations of the **Stock Market Intelligence Dashboard**.

## 1. Data Connection Details
- **Source**: MySQL Database (local/production) or fallback `stock_market_cleaned.csv`.
- **Primary Table**: `stock_market_cleaned`
- **Views Consumed**:
  - `vw_average_close` (Close Price rankings)
  - `vw_price_extremes` (High, Low, and trading volumes)
  - `vw_daily_returns_summary` (Average daily returns, standard deviation risk volatility)

## 2. Page 1: Main Dashboard (Stock Performance Overview)
- **KPI Cards**:
  - **Total Companies**: Distinct count of `Ticker` (value: 5)
  - **Average Close Price**: Average of `Close` column across selected ranges.
  - **Total Volume**: Sum of `Volume` column.
  - **Avg Daily Return**: Average of `Daily_Return` in percent.
- **Charts**:
  - **Stock Price Trend**: Line chart of `Close` price (Y-axis) over `Date` (X-axis), with `Ticker` as Legend. Shows stock growth trajectory.
  - **Outliers & Ranges**: Boxplot displaying `Close` price groupings by `Ticker`.
  - **Slicers**:
    - `Ticker` (Dropdown list filter)
    - `Date` (Relative date range/slider bar)

## 3. Page 2: Trading Volume Analysis
- **Charts**:
  - **Volume Trends**: Area/Line chart of `Volume` over `Date`, grouped by `Ticker`.
  - **Total Volume Share**: Pie/Donut chart illustrating total volume share (%) per ticker.
  - **Avg Daily Volume vs Avg Price**: Scatter plot showing Volume on X-axis and Close Price on Y-axis.

## 4. Page 3: Risk & Monthly Returns Profile
- **Charts**:
  - **Daily Return Distribution**: Histogram of `Daily_Return` showing count frequency.
  - **Risk Volatility Table**: Matrix displaying Ticker, Avg Daily Return, and Volatility (Standard Deviation of returns).
  - **Price Extremes Ranges**: Clustered column chart showing Min Low and Max High prices side-by-side.
