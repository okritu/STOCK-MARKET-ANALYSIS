import pandas as pd
import numpy as np
import pytest
from src.transformation.features import add_technical_indicators
from src.analysis.queries import get_average_close_price, get_daily_returns_summary

def test_add_technical_indicators():
    # Setup data with 2 tickers and multiple dates
    data = {
        "Date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-01", "2023-01-02"]),
        "Ticker": ["AAPL", "AAPL", "MSFT", "MSFT"],
        "Close": [100.0, 105.0, 200.0, 190.0]
    }
    df = pd.DataFrame(data)
    
    transformed = add_technical_indicators(df)
    
    # AAPL day 2: (105 - 100) / 100 * 100 = 5.0%
    # MSFT day 2: (190 - 200) / 200 * 100 = -5.0%
    # The old bug would calculate returns across AAPL and MSFT rows sequentially.
    
    aapl_ret = transformed[transformed["Ticker"] == "AAPL"].sort_values(by="Date").reset_index(drop=True)
    msft_ret = transformed[transformed["Ticker"] == "MSFT"].sort_values(by="Date").reset_index(drop=True)
    
    assert pd.isna(aapl_ret.loc[0, "Daily_Return"])
    assert aapl_ret.loc[1, "Daily_Return"] == 5.0
    
    assert pd.isna(msft_ret.loc[0, "Daily_Return"])
    assert msft_ret.loc[1, "Daily_Return"] == -5.0

def test_analytical_queries():
    data = {
        "Date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-01", "2023-01-02"]),
        "Ticker": ["AAPL", "AAPL", "MSFT", "MSFT"],
        "Close": [100.0, 110.0, 200.0, 210.0],
        "Daily_Return": [np.nan, 10.0, np.nan, 5.0]
    }
    df = pd.DataFrame(data)
    
    avg_close = get_average_close_price(df)
    assert avg_close[avg_close["Ticker"] == "AAPL"]["Avg_Close_Price"].values[0] == 105.0
    assert avg_close[avg_close["Ticker"] == "MSFT"]["Avg_Close_Price"].values[0] == 205.0
    
    summary = get_daily_returns_summary(df)
    assert summary[summary["Ticker"] == "AAPL"]["Avg_Daily_Return"].values[0] == 10.0
    assert summary[summary["Ticker"] == "MSFT"]["Avg_Daily_Return"].values[0] == 5.0
