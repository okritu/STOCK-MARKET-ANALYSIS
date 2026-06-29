import os
import matplotlib.pyplot as plt
import seaborn as sns
from config.config import PLOT_OUTPUT_DIR, REPORTS_CHART_DIR
from src.utilities.logger import setup_logger

logger = setup_logger(__name__)

# Apply Seaborn style
sns.set_theme(style="whitegrid")

def save_plot(fig, filename):
    """
    Saves a matplotlib figure to both reports/charts and output/plots.
    """
    paths = [
        os.path.join(PLOT_OUTPUT_DIR, filename),
        os.path.join(REPORTS_CHART_DIR, filename)
    ]
    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        fig.savefig(p, bbox_inches="tight", dpi=150)
        logger.info(f"Saved chart to: {p}")

def generate_all_plots(df):
    """
    Generates and saves:
    1. Closing Price Trend (grouped by Ticker with legend)
    2. Trading Volume Trend (grouped by Ticker)
    3. Daily Return Distribution (stacked histogram by Ticker)
    4. Close Price Outliers (grouped boxplot)
    """
    logger.info("Generating and saving reporting charts...")
    
    # Check if we have data to plot
    if df.empty:
        logger.warning("Stock DataFrame is empty. No plots generated.")
        return
        
    # Ensure Date column is datetime
    df = df.copy()
    df["Date"] = pd_to_datetime_fallback(df["Date"])
    
    # 1. Closing Price Trend
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    for ticker, group in df.groupby("Ticker"):
        ax1.plot(group["Date"], group["Close"], label=ticker, linewidth=1.5)
    ax1.set_title("Historical Closing Price Trend", fontsize=14, fontweight="bold", pad=15)
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_ylabel("Close Price (USD)", fontsize=12)
    ax1.legend(title="Ticker", frameon=True)
    plt.tight_layout()
    save_plot(fig1, "closing_price_trend.png")
    plt.close(fig1)
    
    # 2. Trading Volume Trend
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    for ticker, group in df.groupby("Ticker"):
        ax2.plot(group["Date"], group["Volume"], label=ticker, alpha=0.7)
    ax2.set_title("Trading Volume Over Time", fontsize=14, fontweight="bold", pad=15)
    ax2.set_xlabel("Date", fontsize=12)
    ax2.set_ylabel("Volume", fontsize=12)
    ax2.legend(title="Ticker", frameon=True)
    plt.tight_layout()
    save_plot(fig2, "trading_volume_trend.png")
    plt.close(fig2)
    
    # 3. Daily Return Distribution
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    df_clean = df.dropna(subset=["Daily_Return"])
    if not df_clean.empty:
        sns.histplot(data=df_clean, x="Daily_Return", hue="Ticker", bins=50, kde=True, ax=ax3, multiple="stack")
    ax3.set_title("Daily Return Distribution", fontsize=14, fontweight="bold", pad=15)
    ax3.set_xlabel("Daily Return (%)", fontsize=12)
    ax3.set_ylabel("Frequency", fontsize=12)
    plt.tight_layout()
    save_plot(fig3, "daily_return_distribution.png")
    plt.close(fig3)
    
    # 4. Close Price Outliers Boxplot
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x="Ticker", y="Close", ax=ax4, palette="Set2")
    ax4.set_title("Close Price Outliers & Distribution by Ticker", fontsize=14, fontweight="bold", pad=15)
    ax4.set_xlabel("Ticker", fontsize=12)
    ax4.set_ylabel("Close Price (USD)", fontsize=12)
    plt.tight_layout()
    save_plot(fig4, "close_price_outliers.png")
    plt.close(fig4)
    
    logger.info("All reporting charts generated successfully.")

def pd_to_datetime_fallback(series):
    import pandas as pd
    return pd.to_datetime(series)
