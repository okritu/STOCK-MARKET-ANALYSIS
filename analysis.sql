CREATE DATABASE stock_market_analysis;
USE stock_market_analysis;
SELECT * FROM stock_market_cleaned;
SELECT COUNT(*)
FROM stock_market_cleaned;
DESCRIBE stock_market_cleaned;
SELECT AVG(Close) FROM stock_market_cleaned; 
SELECT MAX(High)FROM stock_market_cleaned;
SELECT MIN(Low)FROM stock_market_cleaned; 
SELECT AVG(Volume) FROM stock_market_cleaned;

