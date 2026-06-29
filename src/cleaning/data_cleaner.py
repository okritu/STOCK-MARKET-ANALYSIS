import os
import pandas as pd
import numpy as np
from src.utilities.logger import setup_logger
from config.config import CLEANED_DATA_CSV, CLEANED_DATA_OUTPUT

logger = setup_logger(__name__)

def clean_stock_data(df):
    """
    Cleans the stock data:
    1. Stacks ticker level if MultiIndex columns are present.
    2. Renames and standardizes columns safely by name mapping (fixes shift bug).
    3. Handles missing values via forward/backward fill grouped by Ticker.
    4. Drops duplicates.
    5. Casts types correctly.
    """
    logger.info("Starting stock data cleaning process")
    
    # If columns are MultiIndex, stack ticker level (level 1)
    if isinstance(df.columns, pd.MultiIndex):
        logger.info("MultiIndex columns detected. Stacking level 1 (Ticker)...")
        df = df.stack(level=1)
        df = df.reset_index()
    
    logger.info(f"Columns before standardizing: {list(df.columns)}")
    
    # Dynamically map names to prevent shift bugs
    rename_map = {
        "level_1": "Ticker",
        "ticker": "Ticker",
        "Date": "Date",
        "Open": "Open",
        "High": "High",
        "Low": "Low",
        "Close": "Close",
        "Volume": "Volume",
        "Adj Close": "Adj_Close",
        "Adj_Close": "Adj_Close"
    }
    
    df = df.rename(columns=rename_map)
    
    # If Ticker was not mapped, locate the object/string column
    if "Ticker" not in df.columns:
        known_cols = {"Date", "Open", "High", "Low", "Close", "Volume", "Adj_Close"}
        for col in df.columns:
            if col not in known_cols:
                df = df.rename(columns={col: "Ticker"})
                break
                
    # Cast Date to datetime before sorting
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Reorder columns to a clean standard
    standard_cols = ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]
    if "Adj_Close" in df.columns:
        standard_cols.append("Adj_Close")
        
    existing_cols = [c for c in standard_cols if c in df.columns]
    df = df[existing_cols]
    
    logger.info(f"Columns standardized to: {list(df.columns)}")
    
    # Handle missing values grouped by Ticker
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        logger.info(f"Found {missing_count} missing values. Performing ffill/bfill within tickers.")
        for col in df.columns:
            if col not in ["Date", "Ticker"]:
                df[col] = df.groupby("Ticker")[col].transform(lambda x: x.ffill().bfill())

        
    # Handle duplicates
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        logger.info(f"Found {dup_count} duplicate rows. Dropping duplicates.")
        df = df.drop_duplicates()
        
    # Standardize data types
    for col in ["Open", "High", "Low", "Close"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "Volume" in df.columns:
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").fillna(0).astype("int64")
        
    # Sort by Ticker and Date
    df = df.sort_values(by=["Ticker", "Date"]).reset_index(drop=True)
    logger.info(f"Cleaning complete. Output shape: {df.shape}")
    
    return df

def save_clean_data(df, path1=None, path2=None):
    """
    Saves clean stock data to data/processed and output/cleaned_data.
    """
    if path1 is None:
        path1 = CLEANED_DATA_CSV
    if path2 is None:
        path2 = CLEANED_DATA_OUTPUT
        
    for p in [path1, path2]:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        try:
            df.to_csv(p, index=False)
            logger.info(f"Cleaned dataset saved successfully to: {p}")
        except Exception as e:
            logger.error(f"Failed to save cleaned data to {p}: {e}")
            raise
