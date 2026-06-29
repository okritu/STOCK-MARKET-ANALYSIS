USE stock_market_analysis;

-- Query 1: Rank companies by average closing price
SELECT * FROM vw_average_close 
ORDER BY Avg_Close_Price DESC;

-- Query 2: Retrieve stock price extremums and average volumes
SELECT * FROM vw_price_extremes 
ORDER BY Avg_Trading_Volume DESC;

-- Query 3: Analyze daily returns and risk volatility
SELECT * FROM vw_daily_returns_summary 
ORDER BY Volatility_Daily_Return DESC;

-- Query 4: Check data coverage (total transaction days per stock)
SELECT Ticker, COUNT(*) AS Total_Days
FROM stock_market_cleaned
GROUP BY Ticker
ORDER BY Total_Days DESC;
