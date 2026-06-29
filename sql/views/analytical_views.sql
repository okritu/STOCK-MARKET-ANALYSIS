USE stock_market_analysis;

-- 1. Average Close Price by Ticker
CREATE OR REPLACE VIEW vw_average_close AS
SELECT Ticker, AVG(Close) AS Avg_Close_Price
FROM stock_market_cleaned
GROUP BY Ticker;

-- 2. Volatility and Price Extremes
CREATE OR REPLACE VIEW vw_price_extremes AS
SELECT 
    Ticker, 
    MAX(High) AS Max_High_Price, 
    MIN(Low) AS Min_Low_Price,
    AVG(Volume) AS Avg_Trading_Volume
FROM stock_market_cleaned
GROUP BY Ticker;

-- 3. Daily Returns & Risk profile
CREATE OR REPLACE VIEW vw_daily_returns_summary AS
SELECT 
    Ticker, 
    AVG(Daily_Return) AS Avg_Daily_Return,
    MIN(Daily_Return) AS Min_Daily_Return,
    MAX(Daily_Return) AS Max_Daily_Return,
    STDDEV(Daily_Return) AS Volatility_Daily_Return
FROM stock_market_cleaned
WHERE Daily_Return IS NOT NULL
GROUP BY Ticker;
 