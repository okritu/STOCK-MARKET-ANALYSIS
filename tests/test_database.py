import pytest
from sqlalchemy import text
from config.database import get_engine

def test_database_connection():
    engine = get_engine()
    assert engine is not None
    
    # Verify the database connection allows basic queries
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
