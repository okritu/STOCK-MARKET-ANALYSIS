# Contributing to Stock Market Intelligence

Thank you for your interest in contributing! This project is maintained using software engineering best practices. Please follow these guidelines:

## Code of Conduct

Help us maintain a clean, friendly, and respectful environment.

## Development Workflow

1. **Fork the Repository**: Clone the project onto your local machine.
2. **Set up Virtual Environment**:
   ```bash
   conda env create -f environment.yml
   conda activate stock-market-analysis
   # OR using pip:
   python -m venv .venv
   source .venv/bin/activate # On Windows: .venv\Scripts\activate
   make setup
   ```
3. **Run Code Quality Checks**:
   Always lint and check code formatting before submitting pull requests:
   ```bash
   make lint
   ```
4. **Write Tests**:
   If adding ingestion adapters, cleaning constraints, or indicators, write matching tests under `tests/`.
5. **Run the Test Suite**:
   ```bash
   make test
   ```
6. **Submit Pull Requests**:
   Fill in the provided PR template and link matching bug report/feature requests.
