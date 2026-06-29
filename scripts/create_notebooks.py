import os
import json

# Define the notebooks and their cells
notebooks = {
    "01_data_loading.ipynb": [
        ("markdown", "# 01 - Stock Market Data Loading & Ingestion\nThis notebook demonstrates loading raw stock market data from Yahoo Finance and saving it to our raw data repository."),
        ("code", "import sys\nimport os\n# Add the project root directory to the python path\nsys.path.append(os.path.abspath('..'))"),
        ("code", "from src.ingestion.data_loader import fetch_stock_data, save_raw_data\nfrom config.config import TICKERS, START_DATE, END_DATE"),
        ("code", "# Fetch historical data using configuration parameters\nraw_df = fetch_stock_data(tickers=TICKERS, start=START_DATE, end=END_DATE)"),
        ("code", "# Save raw yfinance data (with MultiIndex) to the data/raw folder\nsave_raw_data(raw_df)"),
        ("code", "# Display raw data structure\nraw_df.head()")
    ],
    "02_cleaning.ipynb": [
        ("markdown", "# 02 - Stock Market Data Cleaning & Preprocessing\nThis notebook loads the raw data, standardizes column mappings, executes quality validation checks, calculates financial features, and saves the cleaned dataset."),
        ("code", "import sys\nimport os\nsys.path.append(os.path.abspath('..'))"),
        ("code", "from src.ingestion.data_loader import load_raw_data\nfrom src.cleaning.data_cleaner import clean_stock_data, save_clean_data\nfrom src.validation.quality_check import run_quality_checks\nfrom src.transformation.features import add_technical_indicators"),
        ("code", "# Step 1: Load raw yfinance data preserving MultiIndex columns\nraw_df = load_raw_data()"),
        ("code", "# Step 2: Clean the data (fixes column shift bug)\ncleaned_df = clean_stock_data(raw_df)\ncleaned_df.head()"),
        ("code", "# Step 3: Run data quality constraint verification checks\nrun_quality_checks(cleaned_df)"),
        ("code", "# Step 4: Feature engineering (calculates daily returns grouped correctly by Ticker)\ntransformed_df = add_technical_indicators(cleaned_df)\ntransformed_df.head()"),
        ("code", "# Step 5: Save processed stock market dataset\nsave_clean_data(transformed_df)")
    ],
    "03_eda.ipynb": [
        ("markdown", "# 03 - Exploratory Data Analysis (EDA)\nThis notebook explores the clean stock dataset by computing key descriptive statistics, distributions, and checking correlations."),
        ("code", "import sys\nimport os\nimport pandas as pd\nsys.path.append(os.path.abspath('..'))"),
        ("code", "from config.config import CLEANED_DATA_CSV"),
        ("code", "# Load cleaned dataset\ndf = pd.read_csv(CLEANED_DATA_CSV, parse_dates=['Date'])\ndf.head()"),
        ("code", "# General dataset structure info\ndf.info()"),
        ("code", "# Summary statistics of Close price and Volume\ndf[['Close', 'Volume', 'Daily_Return']].describe()"),
        ("code", "# Descriptive statistics grouped by Ticker\ndf.groupby('Ticker')['Close'].describe()")
    ],
    "04_SQL_analysis.ipynb": [
        ("markdown", "# 04 - SQL Database Analytics\nThis notebook demonstrates running SQL queries against database views to answer key analytical business questions."),
        ("code", "import sys\nimport os\nimport pandas as pd\nfrom sqlalchemy import text\nsys.path.append(os.path.abspath('..'))"),
        ("code", "from config.database import get_engine"),
        ("code", "# Initialize database engine\nengine = get_engine()"),
        ("code", "# Query 1: Rank companies by average close price\nwith engine.connect() as conn:\n    df_avg = pd.read_sql(text('SELECT * FROM vw_average_close ORDER BY Avg_Close_Price DESC'), conn)\ndf_avg"),
        ("code", "# Query 2: Retrieve price extremes & trading volume averages\nwith engine.connect() as conn:\n    df_extremes = pd.read_sql(text('SELECT * FROM vw_price_extremes'), conn)\ndf_extremes"),
        ("code", "# Query 3: Volatility and Risk Profile\nwith engine.connect() as conn:\n    df_returns = pd.read_sql(text('SELECT * FROM vw_daily_returns_summary'), conn)\ndf_returns")
    ],
    "05_visualization.ipynb": [
        ("markdown", "# 05 - Historical Visualizations & Charting\nThis notebook generates historical closing price trends, volume distributions, and risk profiling charts, saving them to reporting folders."),
        ("code", "import sys\nimport os\nimport pandas as pd\nsys.path.append(os.path.abspath('..'))"),
        ("code", "from config.config import CLEANED_DATA_CSV\nfrom src.visualization.charts import generate_all_plots"),
        ("code", "# Load dataset\ndf = pd.read_csv(CLEANED_DATA_CSV)\n# Generate all reporting figures\ngenerate_all_plots(df)")
    ],
    "06_business_insights.ipynb": [
        ("markdown", "# 06 - Stock Investment Business Insights\nThis notebook calculates risk volatility metrics and pricing trends to provide actionable financial recommendations."),
        ("code", "import sys\nimport os\nimport pandas as pd\nsys.path.append(os.path.abspath('..'))"),
        ("code", "from config.config import CLEANED_DATA_CSV\nfrom src.analysis.queries import get_average_close_price, get_daily_returns_summary, get_price_extremes"),
        ("code", "# Load data\ndf = pd.read_csv(CLEANED_DATA_CSV)\n\nprint('=== Average Closing Price Ranking ===')\nprint(get_average_close_price(df).to_string(index=False))"),
        ("code", "print('\n=== Volatility Risk Profile (Returns StdDev) ===')\nprint(get_daily_returns_summary(df).to_string(index=False))"),
        ("code", "print('\n=== Historical Price Ranges and Volumes ===')\nprint(get_price_extremes(df).to_string(index=False))")
    ]
}

def create_notebook(filename, cells):
    nb = {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5
    }
    
    for cell_type, content in cells:
        cell = {
            "cell_type": cell_type,
            "metadata": {},
            "source": [line + "\n" for line in content.split("\n")]
        }
        if cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        nb["cells"].append(cell)
        
    path = os.path.join("notebooks", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"Created notebook: {path}")

if __name__ == "__main__":
    for filename, cells in notebooks.items():
        create_notebook(filename, cells)
