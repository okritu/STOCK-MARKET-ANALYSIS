import pandas as pd
import numpy as np
import pytest
from src.cleaning.data_cleaner import clean_stock_data

def test_clean_stock_data():
    # Construct a sample MultiIndex dataframe mimicking yfinance
    columns = pd.MultiIndex.from_tuples([
        ("Close", "AAPL"), ("Close", "MSFT"),
        ("High", "AAPL"), ("High", "MSFT"),
        ("Low", "AAPL"), ("Low", "MSFT"),
        ("Open", "AAPL"), ("Open", "MSFT"),
        ("Volume", "AAPL"), ("Volume", "MSFT")
    ], names=["Price", "Ticker"])
    
    dates = pd.date_range(start="2023-01-01", periods=3)
    data = [
        [100, 200, 105, 205, 95, 195, 101, 201, 1000, 2000],
        [np.nan, 210, 106, 212, 98, 198, 102, 202, 1010, 2010],
        [102, 208, 107, 210, 97, 197, 103, 203, 1020, 2020]
    ]
    df = pd.DataFrame(data, index=dates, columns=columns)
    df.index.name = "Date"
    
    cleaned = clean_stock_data(df)
    
    # Assert columns are labeled correctly and order is standard (no shift bug!)
    expected_cols = ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]
    assert list(cleaned.columns) == expected_cols
    
    # Assert NaN values filled
    aapl_rows = cleaned[cleaned["Ticker"] == "AAPL"].sort_values(by="Date").reset_index(drop=True)
    assert aapl_rows.loc[1, "Close"] == 100.0
    
    # Assert both tickers parsed
    assert set(cleaned["Ticker"]) == {"AAPL", "MSFT"}
