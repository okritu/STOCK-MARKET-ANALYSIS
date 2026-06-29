import os
import logging
from config.config import LOG_FILE_PATH, ERROR_LOG_PATH

def setup_logger(name=__name__):
    """
    Configures and returns a logger instance.
    Logs INFO+ to console and pipeline.log, and WARNING+ to errors.log.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
        
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File Handler (all logs)
    file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Error Handler (warning + errors only)
    error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding="utf-8")
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger
