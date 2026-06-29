import os
import pandas as pd
import yfinance as yf
from config.config import TICKERS, START_DATE, END_DATE, RAW_DATA_PATH
from src.utilities.logger import setup_logger

logger = setup_logger(__name__)

def fetch_stock_data(tickers=None, start=None, end=None):
    """
    Downloads historical stock market data from Yahoo Finance for a list of tickers.
    """
    if tickers is None:
        tickers = TICKERS
    if start is None:
        start = START_DATE
    if end is None:
        end = END_DATE
        
    logger.info(f"Downloading data from Yahoo Finance for tickers: {tickers} ({start} to {end})")
    
    try:
        df = yf.download(tickers, start=start, end=end)
        if df.empty:
            raise ValueError("Downloaded stock DataFrame is empty. Verify tickers and date ranges.")
        logger.info(f"Successfully downloaded stock data of shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error during stock data download: {e}")
        raise

def save_raw_data(df, output_path=None):
    """
    Saves raw downloaded stock data to CSV, maintaining MultiIndex.
    """
    if output_path is None:
        output_path = RAW_DATA_PATH
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        df.to_csv(output_path)
        logger.info(f"Raw data successfully saved to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save raw data to {output_path}: {e}")
        raise

def load_raw_data(input_path=None):
    """
    Loads raw stock data from CSV preserving MultiIndex structure.
    """
    if input_path is None:
        input_path = RAW_DATA_PATH
    logger.info(f"Loading raw stock data from: {input_path}")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Raw stock data CSV not found at: {input_path}")
    return pd.read_csv(input_path, header=[0, 1], index_col=0, parse_dates=True)
