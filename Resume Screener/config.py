"""
Configuration module for Resume Screener.

Handles API configuration, rate limiting, and logging setup.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (in a real application, these would be read from environment variables)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")  # For accessing DeepSeek

# Rate limiting (seconds between API calls to respect the 10 calls per minute limit)
API_RATE_LIMIT = 6  # 60 seconds / 10 calls = 6 seconds per call

# Logging configuration
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
LOG_FILE = os.path.join(
    LOG_DIR, f"resume_screener_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_MAX_SIZE = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3


def setup_logging():
    """Set up logging with rotation and proper formatting."""

    # Create logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # Clear existing handlers
    if logger.handlers:
        logger.handlers.clear()

    # Create rotating file handler
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP_COUNT
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
