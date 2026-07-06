"""
=========================================================
AI-Enhanced SOC Analytics Platform
Logging Module
---------------------------------------------------------
This module configures logging for the entire project.

Author : Abdul Fathah
Project: AI-Enhanced SOC Analytics Platform
=========================================================
"""

import logging
from pathlib import Path

# -------------------------------------------------------
# Create logs directory if it doesn't exist
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "soc_platform.log"

# -------------------------------------------------------
# Configure Logger
# -------------------------------------------------------

logger = logging.getLogger("SOC_PLATFORM")

logger.setLevel(logging.INFO)

# Prevent duplicate log messages
if not logger.handlers:

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Write logs to file
    file_handler = logging.FileHandler(LOG_FILE)

    file_handler.setLevel(logging.INFO)

    file_handler.setFormatter(formatter)

    # Display logs in terminal
    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)

    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)

    logger.addHandler(console_handler)


# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------

def log_info(message):
    logger.info(message)


def log_warning(message):
    logger.warning(message)


def log_error(message):
    logger.error(message)


def log_critical(message):
    logger.critical(message)


# -------------------------------------------------------
# Test Logger
# -------------------------------------------------------

if __name__ == "__main__":

    log_info("SOC Platform Started")

    log_warning("Sample Warning")

    log_error("Sample Error")

    log_critical("Sample Critical Error")