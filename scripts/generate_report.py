import os
import sys
import pandas as pd

# Add the project root to sys.path to allow importing local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import CLEANED_DATA_CSV, WORKSPACE_ROOT
from src.analysis.queries import get_average_close_price, get_daily_returns_summary
from src.utilities.logger import setup_logger

logger = setup_logger(__name__)

def generate_report():
    logger.info("Starting automated analytical report generation...")
    if not os.path.exists(CLEANED_DATA_CSV):
        logger.error(f"Cleaned CSV not found at: {CLEANED_DATA_CSV}. Run pipeline first.")
        return
        
    df = pd.read_csv(CLEANED_DATA_CSV)
    avg_close = get_average_close_price(df)
    volatility = get_daily_returns_summary(df)
    
    report_path = os.path.join(WORKSPACE_ROOT, "reports/figures/analytical_report.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write("# Automated Stock Market Intelligence Report\n\n")
        f.write("This report compiles historical price averages and returns volatility metrics.\n\n")
        f.write("## 1. Stock Price Valuations (Average Close Price)\n\n")
        f.write(avg_close.to_markdown(index=False) + "\n\n")
        f.write("## 2. Risk & Volatility Profile (Returns Standard Deviation)\n\n")
        f.write(volatility.to_markdown(index=False) + "\n\n")
        f.write("## 3. Visual Performance Trends\n\n")
        f.write("- Closing Price Trend:\n  ![Closing Price Trend](../charts/closing_price_trend.png)\n")
        f.write("- Daily Return Distribution:\n  ![Daily Return Distribution](../charts/daily_return_distribution.png)\n")
        
    logger.info(f"Analytical report successfully saved to: {report_path}")

if __name__ == "__main__":
    generate_report()
