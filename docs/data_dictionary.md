# Data Dictionary

This document describes the schema structure of the cleaned and transformed dataset `stock_market_cleaned` stored in MySQL and exported as CSV.

| Field Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| **Date** | DATE | Primary Key (Composite) | The trading day of the stock record (YYYY-MM-DD). |
| **Ticker** | VARCHAR(10) | Primary Key (Composite) | The ticker symbol representing the company (e.g., AAPL, MSFT, TSLA, GOOGL, AMZN). |
| **Open** | DOUBLE / FLOAT | - | The price of the stock when the market opened for that trading day. |
| **High** | DOUBLE / FLOAT | - | The maximum price reached by the stock during that trading day. |
| **Low** | DOUBLE / FLOAT | - | The minimum price reached by the stock during that trading day. |
| **Close** | DOUBLE / FLOAT | - | The final transaction price of the stock when the market closed for the day. |
| **Volume** | BIGINT / INT | - | The total number of shares traded during that day. |
| **Daily_Return** | DOUBLE / FLOAT | - | The percentage return change in Close price compared to the previous trading day for that specific Ticker. Null for the first trading day. |
| **MA_20** | DOUBLE / FLOAT | - | The 20-day Simple Moving Average (SMA) of Close price calculated grouped by Ticker. Null for the first 19 trading days. |
