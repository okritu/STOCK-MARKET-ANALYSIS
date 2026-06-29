import pandas as pd
from src.utilities.logger import setup_logger

logger = setup_logger(__name__)

def get_average_close_price(df):
    """
    Calculates average closing price grouped by Ticker.
    """
    logger.info("Calculating average closing price by ticker...")
    return df.groupby("Ticker")["Close"].mean().reset_index().rename(
        columns={"Close": "Avg_Close_Price"}
    ).sort_values(by="Avg_Close_Price", ascending=False)

def get_price_extremes(df):
    """
    Retrieves Max High, Min Low, and Average Volume by Ticker.
    """
    logger.info("Calculating price extremes and average volume by ticker...")
    return df.groupby("Ticker").agg(
        Max_High_Price=("High", "max"),
        Min_Low_Price=("Low", "min"),
        Avg_Trading_Volume=("Volume", "mean")
    ).reset_index()

def get_daily_returns_summary(df):
    """
    Calculates average, min, max, and volatility of daily returns by Ticker.
    """
    logger.info("Calculating daily returns statistics and volatility by ticker...")
    if "Daily_Return" not in df.columns:
        raise ValueError("Daily_Return column is missing from the DataFrame.")
    return df.dropna(subset=["Daily_Return"]).groupby("Ticker").agg(
        Avg_Daily_Return=("Daily_Return", "mean"),
        Min_Daily_Return=("Daily_Return", "min"),
        Max_Daily_Return=("Daily_Return", "max"),
        Volatility_Daily_Return=("Daily_Return", "std")
    ).reset_index()
