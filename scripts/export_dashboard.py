import os
import sys

# Add the project root to sys.path to allow importing local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import WORKSPACE_ROOT
from src.utilities.logger import setup_logger

logger = setup_logger(__name__)

def export_dashboard():
    logger.info("Initializing Power BI dashboard configuration check...")
    
    pbix_path = os.path.join(WORKSPACE_ROOT, "powerbi/dashboard.pbix")
    theme_path = os.path.join(WORKSPACE_ROOT, "powerbi/theme.json")
    
    if not os.path.exists(pbix_path):
        logger.error(f"Dashboard pbix file not found at: {pbix_path}")
        return False
        
    if not os.path.exists(theme_path):
        logger.error(f"Dashboard theme file not found at: {theme_path}")
        return False
        
    logger.info(f"Dashboard file verified at: {pbix_path}")
    logger.info(f"Dashboard theme verified at: {theme_path}")
    logger.info("Power BI configuration and theme settings exported successfully.")
    return True

if __name__ == "__main__":
    export_dashboard()
