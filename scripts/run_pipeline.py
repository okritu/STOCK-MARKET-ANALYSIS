import sys
import os
from sqlalchemy import text

# Add the project root to sys.path to allow importing local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DB_TABLE
from config.database import get_engine
from src.utilities.logger import setup_logger
from src.ingestion.data_loader import fetch_stock_data, save_raw_data
from src.cleaning.data_cleaner import clean_stock_data, save_clean_data
from src.validation.quality_check import run_quality_checks
from src.transformation.features import add_technical_indicators
from src.visualization.charts import generate_all_plots
from src.analysis.queries import get_average_close_price, get_daily_returns_summary
from scripts.setup_database import setup_db

logger = setup_logger(__name__)

def run_pipeline():
    """
    Main orchestrator for the stock market analytics data pipeline.
    """
    logger.info("=========================================")
    logger.info("Starting Stock Market Dashboard Pipeline")
    logger.info("=========================================")
    
    try:
        # Step 1: Ingestion
        raw_df = fetch_stock_data()
        save_raw_data(raw_df)
        
        # Step 2: Cleaning (Fixes Column Shift Bug)
        cleaned_df = clean_stock_data(raw_df)
        
        # Step 3: Validation
        if not run_quality_checks(cleaned_df):
            logger.error("Pipeline stopped due to data validation failures.")
            sys.exit(1)
            
        # Step 4: Feature Transformation (Fixes Daily Return calculations)
        transformed_df = add_technical_indicators(cleaned_df)
        
        # Step 5: Save Cleaned Datasets
        save_clean_data(transformed_df)
        
        # Step 6: Initialize Database Schema (DDL)
        setup_db()
        
        # Step 7: Load Data to SQL (preserving schemas & PKs)
        engine = get_engine()
        logger.info(f"Uploading cleaned stock market data to table: {DB_TABLE}")
        with engine.begin() as conn:
            # Delete old records to prevent duplicate key errors during append
            conn.execute(text(f"DELETE FROM {DB_TABLE}"))
        
        # Append clean data to the pre-created schema
        transformed_df.to_sql(DB_TABLE, engine, if_exists="append", index=False)
        logger.info("Data successfully loaded into SQL database.")
        
        # Step 8: Generate Reports & Visualizations
        generate_all_plots(transformed_df)
        
        # Step 9: Sample Query Logging
        logger.info("Running sample analysis queries...")
        avg_close = get_average_close_price(transformed_df)
        logger.info("\n" + avg_close.to_string(index=False))
        
        returns_summary = get_daily_returns_summary(transformed_df)
        logger.info("\n" + returns_summary.to_string(index=False))
        
        logger.info("=========================================")
        logger.info("Pipeline executed and completed successfully!")
        logger.info("=========================================")
        
    except Exception as e:
        logger.critical(f"Pipeline execution failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
