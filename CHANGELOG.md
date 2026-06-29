# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-29

### Added
- Created production-grade, modular folder structure separating config, raw data, logs, and processed outputs.
- Developed dynamic configuration loaders using `config/settings.yaml` and `config/config.py`.
- Implemented robust database connector in `config/database.py` with an automatic MySQL-to-SQLite connection fallback.
- Added structured logging utility writing to `logs/pipeline.log` and warning/errors to `logs/errors.log`.
- Created an end-to-end data pipeline script `scripts/run_pipeline.py` orchestrating yfinance ingestion, data cleaning, and database loading.
- Added SQL database schema initialization routines in `scripts/setup_database.py`.
- Developed SQL DDL table schemas, business views, and ranking queries under `sql/`.
- Written data quality validation rules in `src/validation/quality_check.py`.
- Implemented Python test suites under `tests/` verifying data ingestion, calculations, and connections.
- Set up automated GitHub Actions workflow in `.github/workflows/ci.yml`.
- Created professional developer documentation (`docs/`, `CONTRIBUTING.md`, `LICENSE`, `CHANGELOG.md`).

### Fixed
- **Fixed Column Shift Bug**: Corrected stacking column renaming logic in `src/cleaning/data_cleaner.py`. Standardized columns by name mapping rather than index list replacements, stopping stock symbols from getting stored in price column variables.
- **Fixed Daily Return Bug**: Grouped closing price percentage change computations by Ticker instead of executing sequentially across different stock series, returning meaningful risk/volatility profiles.
- **Mislabeled SQL Aggregations**: Standardized SQL view mappings to compile statistics on corrected close/low/high columns.
