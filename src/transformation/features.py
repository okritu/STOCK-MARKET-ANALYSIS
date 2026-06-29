import pandas as pd
from src.utilities.logger import setup_logger

logger = setup_logger(__name__)

def add_technical_indicators(df):
    """
    Computes technical indicators grouped by Ticker:
    1. Daily Return: percent change of Close price (grouped by Ticker, in %).
    2. MA_20: 20-day Simple Moving Average of Close price (grouped by Ticker).
    """
    logger.info("Computing technical indicators (Daily_Return, MA_20)")
    
    # Ensure sorting is correct before rolling/percent change calculations
    df = df.sort_values(by=["Ticker", "Date"]).reset_index(drop=True)
    
    # Group by Ticker and calculate returns
    df["Daily_Return"] = df.groupby("Ticker")["Close"].pct_change() * 100
    
    # Group by Ticker and calculate 20-day moving average
    df["MA_20"] = df.groupby("Ticker")["Close"].transform(lambda x: x.rolling(window=20).mean())
    
    logger.info("Technical indicators successfully computed.")
    return df
