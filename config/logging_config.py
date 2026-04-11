# ============================================
# LOGGING CONFIGURATION
# ============================================

import sys
from pathlib import Path
from loguru import logger
from config.settings import settings


def setup_logging():
    """
    Configure loguru logger for the entire application.
    Logs go to both terminal and a log file.
    """

    # Remove default logger
    logger.remove()

    # --- Terminal Logging (colored, readable) ---
    logger.add(
        sys.stdout,
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        level="DEBUG" if settings.DEBUG_MODE else "INFO",
    )

    # --- File Logging (full details saved) ---
    log_path = Path(settings.LOGS_PATH)
    log_path.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_path / "app.log",
        rotation="10 MB",       # New file every 10MB
        retention="7 days",     # Keep logs for 7 days
        compression="zip",      # Compress old logs
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{line} | "
            "{message}"
        ),
        level="DEBUG",
    )

    # --- Separate error log file ---
    logger.add(
        log_path / "errors.log",
        rotation="5 MB",
        retention="30 days",
        compression="zip",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{line} | "
            "{message}"
        ),
        level="ERROR",
    )

    logger.info("✅ Logging configured successfully")
    return logger


# --- Initialize on import ---
setup_logging()