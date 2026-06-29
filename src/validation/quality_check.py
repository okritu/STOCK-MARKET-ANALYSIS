import pandas as pd
from src.utilities.logger import setup_logger

logger = setup_logger(__name__)

def run_quality_checks(df):
    """
    Validates data quality:
    1. Checks if the DataFrame is empty.
    2. Verifies required columns exist.
    3. Checks for negative stock prices.
    4. Checks for negative trading volumes.
    5. Checks for logical inconsistencies (High < Low).
    """
    logger.info("Running data quality validation checks...")
    
    if df.empty:
        logger.error("Validation Failed: Stock DataFrame is empty.")
        return False
        
    required_cols = {"Date", "Ticker", "Open", "High", "Low", "Close", "Volume"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        logger.error(f"Validation Failed: Missing required columns: {missing_cols}")
        return False
        
    # Check negative prices
    price_cols = ["Open", "High", "Low", "Close"]
    for col in price_cols:
        neg_prices = df[df[col] < 0]
        if not neg_prices.empty:
            logger.warning(f"Validation Warning: Found {len(neg_prices)} rows with negative values in {col} column.")
            
    # Check negative volume
    neg_volume = df[df["Volume"] < 0]
    if not neg_volume.empty:
        logger.warning(f"Validation Warning: Found {len(neg_volume)} rows with negative Volume.")
        
    # Check if High is always >= Low
    mismatched_high_low = df[df["High"] < df["Low"]]
    if not mismatched_high_low.empty:
        logger.warning(f"Validation Warning: Found {len(mismatched_high_low)} rows where High price is less than Low price.")
        
    logger.info("Data quality validation checks completed.")
    return True
