import os
import re
from sqlalchemy import text
from config.database import get_engine
from config.config import WORKSPACE_ROOT
from src.utilities.logger import setup_logger

logger = setup_logger(__name__)

def execute_sql_file(conn, file_path, is_sqlite=False):
    """
    Reads an SQL file and executes statements sequentially,
    filtering out MySQL-specific commands if SQLite is used.
    """
    if not os.path.exists(file_path):
        logger.error(f"SQL file not found: {file_path}")
        return
        
    logger.info(f"Executing SQL file: {file_path}")
    with open(file_path, "r") as f:
        content = f.read()
        
    # Split queries by semicolon
    statements = content.split(";")
    
    for statement in statements:
        statement = statement.strip()
        if not statement:
            continue
            
        # SQLite adjustments
        if is_sqlite:
            upper_statement = statement.upper()
            if upper_statement.startswith("USE ") or upper_statement.startswith("CREATE DATABASE"):
                logger.info(f"Skipping database selection/creation for SQLite: '{statement}'")
                continue
            if "CREATE OR REPLACE VIEW" in upper_statement:
                view_name_match = re.search(r"VIEW\s+(\w+)", statement, re.IGNORECASE)
                if view_name_match:
                    view_name = view_name_match.group(1)
                    try:
                        conn.execute(text(f"DROP VIEW IF EXISTS {view_name}"))
                    except Exception:
                        pass
                statement = statement.replace("CREATE OR REPLACE VIEW", "CREATE VIEW")
                
        try:
            conn.execute(text(statement))
        except Exception as e:
            logger.error(f"Failed to execute statement: {statement}. Error: {e}")
            raise

def setup_db():
    """
    Initializes database tables and analytical views.
    """
    engine = get_engine()
    is_sqlite = "sqlite" in str(engine.url)
    
    schema_file = os.path.join(WORKSPACE_ROOT, "sql/schema/create_tables.sql")
    views_file = os.path.join(WORKSPACE_ROOT, "sql/views/analytical_views.sql")
    
    logger.info("Initializing database schema...")
    try:
        with engine.begin() as conn:
            execute_sql_file(conn, schema_file, is_sqlite)
            execute_sql_file(conn, views_file, is_sqlite)
        logger.info("Database schemas and views successfully initialized.")
    except Exception as e:
        logger.critical(f"Database setup failed: {e}")
        raise

if __name__ == "__main__":
    setup_db()
