# System Architecture & Data Flow

This document details the software architecture and component relationships for the Stock Market Dashboard pipeline.

## 1. Directory Blueprint

- **`config/`**: System environments, DB connection endpoints, file routes, and credentials configurations.
- **`src/`**: Modular logic package containing ingestion, cleaning, transformation, validation, and analytics code.
- **`scripts/`**: Orchestration scripts (triggers and setup actions).
- **`sql/`**: Relational schemas, view aggregates, and analytic scripts.
- **`tests/`**: Unit test suite verifying modules against expected rules.
- **`data/`**: Subdivided storage (raw dataset copies, processed CSVs, interim samples).

## 2. Component Design & Code Flow

```mermaid
graph TD
    A[Yahoo Finance API] -->|yfinance.download| B(data_loader.py)
    B -->|Writes raw data| C[data/raw/stock_market_raw.csv]
    C -->|Reads raw data| D(data_cleaner.py)
    D -->|Validates rules| E(quality_check.py)
    D -->|Calculates Daily_Return & MA_20| F(features.py)
    F -->|Writes processed data| G[data/processed/stock_market_cleaned.csv]
    G -->|Uploads table| H[(SQL Database Table)]
    H -->|Compiles metrics| I[SQL Analytical Views]
    G -->|Renders charts| J(charts.py)
    J -->|Saves figures| K[reports/charts/]
    G -->|Pandas queries| L(queries.py)
```

## 3. Orchestrator (`run_pipeline.py`)

The main workflow script wraps this entire execution loop in exception handlers and structured logging statements:
1. `fetch_stock_data()` and `save_raw_data()` from `src.ingestion`.
2. `clean_stock_data()` from `src.cleaning`.
3. `run_quality_checks()` from `src.validation`.
4. `add_technical_indicators()` from `src.transformation`.
5. `save_clean_data()` from `src.cleaning`.
6. `setup_db()` from `scripts` to init schemas and views.
7. Database `append` to populate SQL table.
8. `generate_all_plots()` from `src.visualization`.
9. Log query outputs from `src.analysis.queries`.
