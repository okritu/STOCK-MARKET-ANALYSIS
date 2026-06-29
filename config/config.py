import os
import yaml

# Determine path to settings.yaml relative to this config.py file
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(CONFIG_DIR, "settings.yaml")

def load_settings(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found at: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)

# Load settings
_settings = load_settings(SETTINGS_PATH)

# Expose configs
DB_CONFIG = _settings.get("database", {})
INGESTION_CONFIG = _settings.get("ingestion", {})
PATH_CONFIG = _settings.get("paths", {})

# Database config
DB_DRIVER = DB_CONFIG.get("driver", "mysql+pymysql")
DB_HOST = DB_CONFIG.get("host", "localhost")
DB_PORT = DB_CONFIG.get("port", 3306)
DB_USER = DB_CONFIG.get("user", "root")
DB_PASSWORD = DB_CONFIG.get("password", "")
DB_NAME = DB_CONFIG.get("name", "stock_market_analysis")
DB_TABLE = DB_CONFIG.get("table_name", "stock_market_cleaned")

# Database connection URL
if DB_PASSWORD:
    DB_URI = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DB_URI = f"{DB_DRIVER}://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Ingestion configs
TICKERS = INGESTION_CONFIG.get("tickers", ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"])
START_DATE = INGESTION_CONFIG.get("start_date", "2023-01-01")
END_DATE = INGESTION_CONFIG.get("end_date", "2025-01-01")

# Path configs (Absolute Paths derived from workspace root)
WORKSPACE_ROOT = os.path.dirname(CONFIG_DIR)

RAW_DATA_PATH = os.path.join(WORKSPACE_ROOT, PATH_CONFIG.get("raw_data_path", "data/raw/stock_market_raw.csv"))
CLEANED_DATA_CSV = os.path.join(WORKSPACE_ROOT, PATH_CONFIG.get("cleaned_data_csv", "data/processed/stock_market_cleaned.csv"))
CLEANED_DATA_OUTPUT = os.path.join(WORKSPACE_ROOT, PATH_CONFIG.get("cleaned_data_output", "output/cleaned_data/stock_market_cleaned.csv"))
PLOT_OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, PATH_CONFIG.get("plot_output_dir", "output/plots/"))
REPORTS_CHART_DIR = os.path.join(WORKSPACE_ROOT, PATH_CONFIG.get("reports_chart_dir", "reports/charts/"))
LOG_FILE_PATH = os.path.join(WORKSPACE_ROOT, PATH_CONFIG.get("log_file_path", "logs/pipeline.log"))
ERROR_LOG_PATH = os.path.join(WORKSPACE_ROOT, PATH_CONFIG.get("error_log_path", "logs/errors.log"))
