# 📈 Stock Market Intelligence Dashboard

An end-to-end, production-grade data analytics and engineering platform that ingests historical stock market data, standardizes observations, computes financial metrics, and loads observations into an analytical database for dashboard consumption.

---

## 🔍 Major Refactoring Highlights & Bug Fixes

This project was completely refactored from a monolithic script into an industry-standard production architecture. During refactoring, **two critical analytical bugs** were discovered and resolved:
1. **Column Mapping Correction (Shift Bug)**: Standard yfinance stacked output structures metrics sequentially. The original script hardcoded names, resulting in stock Ticker symbols mapped to the `Open` price variable, Close prices to `High`, High to `Low`, and so on. We replaced this with name-based pandas remapping (`src/cleaning/data_cleaner.py`), restoring true pricing values.
2. **Grouped Daily Returns Calculation**: Daily returns were previously computed across different stocks sequentially (e.g. comparing Amazon's price to Apple's). We grouped observations by Ticker and sorted by Date, yielding mathematically correct returns on the actual closing price (`src/transformation/features.py`).

---

## 📂 Project Structure

```
Project_Name/
│
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .vscode/
│   ├── settings.json
│   ├── launch.json
│   └── extensions.json
│
├── assets/
│   ├── images/
│   ├── gifs/
│   ├── icons/
│   └── logos/
│
├── config/
│   ├── config.py
│   ├── settings.yaml
│   └── database.py
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── external/
│   └── sample/
│
├── notebooks/
│   ├── 01_data_loading.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_EDA.ipynb
│   ├── 04_SQL_analysis.ipynb
│   ├── 05_visualization.ipynb
│   └── 06_business_insights.ipynb
│
├── sql/
│   ├── schema/
│   ├── cleaning/
│   ├── analysis/
│   ├── views/
│   └── stored_procedures/
│
├── powerbi/
│   ├── dashboard.pbix (moves stock_market_intelligence.pbix)
│   ├── theme.json
│   └── screenshots/
│
├── src/
│   ├── __init__.py
│   ├── ingestion/
│   ├── preprocessing/
│   ├── cleaning/
│   ├── transformation/
│   ├── analysis/
│   ├── visualization/
│   ├── utilities/
│   ├── validation/
│   └── helpers/
│
├── reports/
│   ├── figures/
│   ├── charts/
│   ├── dashboards/
│   ├── pdf/
│   └── presentation/
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_analysis.py
│   ├── test_utils.py
│   └── test_database.py
│
├── docs/
│   ├── methodology.md
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── dashboard_documentation.md
│   └── business_questions.md
│
├── logs/
│   ├── pipeline.log
│   └── errors.log
│
├── output/
│   ├── cleaned_data/
│   ├── csv/
│   ├── excel/
│   ├── plots/
│   └── models/
│
├── scripts/
│   ├── run_pipeline.py
│   ├── generate_report.py
│   ├── setup_database.py
│   └── export_dashboard.py
│
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── environment.yml
├── Makefile
├── LICENSE
├── .gitignore
└── CHANGELOG.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Data Preprocessing & Modeling |
| Pandas | High-performance stock manipulation |
| NumPy | Mathematical calculations |
| Matplotlib / Seaborn | Publication-ready visual charting |
| SQLAlchemy / PyMySQL | SQL ingestion connector |
| MySQL | Analytical data warehousing |
| SQLite | Fallback testing database engine |
| Power BI | Interactive business dashboarding |
| Pytest | Automated code library validation |
| GitHub Actions | Automated linting & testing workflow |

---

## 🔄 Data Pipeline Workflow

```
Raw Stock Download (yfinance API)
              │
              ▼
    Save Raw Data (data/raw/)
              │
              ▼
   Reshaping & Cleaning (src/cleaning)
              │
              ▼
  Daily Return & MA Features (src/transformation)
              │
              ▼
   Data Quality Check (src/validation)
              │
              ▼
 MySQL Ingestion / SQLite Fallback (config/database)
              │
              ▼
   SQL Analytical Views Creation (sql/views)
              │
              ▼
Power BI Dashboard / Automated Reports (reports/charts)
```

---

## 🚀 Installation & Local Setup

### 1. Clone & Navigate to Project
```bash
git clone https://github.com/yourusername/STOCK-MARKET-ANALYSIS.git
cd STOCK-MARKET-ANALYSIS
```

### 2. Configure Environment

Using **Conda**:
```bash
conda env create -f environment.yml
conda activate stock-market-analysis
```

Using **pip/Makefile**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
make setup
```

### 3. Run the Data Pipeline
```bash
make run
# OR
python scripts/run_pipeline.py
```
This runs the ingestion downloads, cleans, performs validation checks, uploads to SQL, and exports reporting plots.

### 4. Execute Unit Tests
```bash
make test
# OR
pytest tests/
```

---

## 🗄️ SQL Schema & View Analysis

We compile key business indicators in SQL views for easy report integration:
- `vw_average_close`: Ranks company close price averages.
- `vw_price_extremes`: Analyzes stock liquidity and extremums.
- `vw_daily_returns_summary`: Calculates average return and risk volatility.

Run analysis queries using:
```bash
mysql -u root -p < sql/analysis/analysis_queries.sql
```

---

## 📊 Business Insights

Based on the corrected data (2023-01-01 to 2025-01-01):
1. **Microsoft (MSFT)** holds the highest average closing valuation over the two-year period.
2. **Tesla (TSLA)** exhibits the highest returns volatility, presenting the greatest trading risk profiles but also the highest single-day gains.
3. **Apple (AAPL)** remains highly liquid with consistent trading volumes.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
