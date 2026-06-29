import os
import pytest
import config.config as cfg

def test_config_paths():
    assert cfg.DB_NAME == "stock_market_analysis"
    assert cfg.TICKERS == ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
    assert cfg.START_DATE == "2023-01-01"
    assert cfg.END_DATE == "2025-01-01"
    
    # Assert workspace configurations resolve paths correctly
    assert os.path.exists(cfg.SETTINGS_PATH)
