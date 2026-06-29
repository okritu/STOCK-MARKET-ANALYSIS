# Business Questions & Analytical Insights

This document outlines the business questions answered by the analytical schemas and queries, providing SQL and Pandas implementations for each.

---

### Question 1: What is the historical average closing price for each stock, and which company has the highest valuation?

**SQL Solution:**
```sql
SELECT Ticker, Avg_Close_Price
FROM vw_average_close
ORDER BY Avg_Close_Price DESC;
```

**Pandas Solution:**
```python
from src.analysis.queries import get_average_close_price
print(get_average_close_price(df))
```

---

### Question 2: What are the historical maximum and minimum transaction bounds for each stock, and how do they relate to liquidity?

**SQL Solution:**
```sql
SELECT Ticker, Max_High_Price, Min_Low_Price, Avg_Trading_Volume
FROM vw_price_extremes
ORDER BY Avg_Trading_Volume DESC;
```

**Pandas Solution:**
```python
from src.analysis.queries import get_price_extremes
print(get_price_extremes(df))
```

---

### Question 3: Which ticker presents the highest investment risk (returns volatility) and what is the typical daily return rate?

**SQL Solution:**
```sql
SELECT Ticker, Avg_Daily_Return, Volatility_Daily_Return
FROM vw_daily_returns_summary
ORDER BY Volatility_Daily_Return DESC;
```

**Pandas Solution:**
```python
from src.analysis.queries import get_daily_returns_summary
print(get_daily_returns_summary(df))
```

---

### Question 4: Do we have complete transaction records for all companies across the 2-year analysis window (2023-01-01 to 2025-01-01)?

**SQL Solution:**
```sql
SELECT Ticker, COUNT(*) AS Total_Days
FROM stock_market_cleaned
GROUP BY Ticker
ORDER BY Total_Days DESC;
```

**Pandas Solution:**
```python
print(df.groupby('Ticker')['Date'].count())
```
