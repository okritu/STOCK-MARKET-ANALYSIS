USE stock_market_analysis;

DROP TABLE IF EXISTS stock_market_cleaned;

CREATE TABLE stock_market_cleaned (
    Date DATE NOT NULL,
    Ticker VARCHAR(10) NOT NULL,
    Open DOUBLE,
    High DOUBLE,
    Low DOUBLE,
    Close DOUBLE,
    Volume BIGINT,
    Daily_Return DOUBLE,
    MA_20 DOUBLE,
    PRIMARY KEY (Date, Ticker)
);
