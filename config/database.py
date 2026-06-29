import os
import logging
from sqlalchemy import create_engine
from config.config import DB_URI, DB_NAME, DB_HOST, DB_USER, WORKSPACE_ROOT

logger = logging.getLogger(__name__)

def get_engine():
    """
    Creates and returns a SQLAlchemy database engine.
    If the default MySQL connection fails, falls back to a local SQLite database.
    """
    # Check if mysql connection is usable
    if "mysql" in DB_URI:
        try:
            logger.info(f"Attempting connection to MySQL: {DB_NAME} on {DB_HOST} as {DB_USER}")
            engine = create_engine(DB_URI, connect_args={"connect_timeout": 3})
            # Test the connection quickly
            with engine.connect() as conn:
                pass
            logger.info("Successfully connected to MySQL database.")
            return engine
        except Exception as e:
            logger.warning(
                f"Failed to connect to MySQL database at {DB_HOST}: {e}. "
                "Falling back to local SQLite database for verification and execution."
            )
    
    # SQLite fallback setup
    sqlite_path = os.path.join(WORKSPACE_ROOT, "stock_market_analysis.db")
    sqlite_uri = f"sqlite:///{sqlite_path}"
    logger.info(f"Using SQLite database fallback at: {sqlite_path}")
    return create_engine(sqlite_uri)
