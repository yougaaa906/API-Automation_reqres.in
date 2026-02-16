# -*- coding: utf-8 -*-
"""
Logging configuration for API automation testing
Standard for enterprise-level QA automation framework
"""
import logging
import os
from datetime import datetime

# Create log directory if not exists
LOG_DIR = "./logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file name (with timestamp for CI traceability)
LOG_FILE = f"{LOG_DIR}/api_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure root logger
def setup_logger():
    """
    Setup standard logger for API automation:
    - Console handler (INFO level, simple format)
    - File handler (DEBUG level, detailed format)
    """
    # Root logger configuration
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Base level: DEBUG

    # Console handler (for local/CI console output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)

    # File handler (for persistent log storage)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to logger (avoid duplicate logs)
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Initialize logger (global usage)
logger = setup_logger()
