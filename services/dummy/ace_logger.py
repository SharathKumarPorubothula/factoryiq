"""
FactoryIQ Common Logger
-----------------------

Common logging utility for all FactoryIQ services.

Usage:

    from ace_logger import get_logger

    logger = get_logger(__name__)

    logger.info("Application started")
    logger.warning("Something may be wrong")
    logger.error("Something went wrong")
    logger.exception("Unexpected exception")

The logger writes to:
    1. Console (stdout) - Docker captures this
    2. Optional file - /var/log/factoryiq/<service>.log

Environment variables:

    SERVICE_NAME
        Name of the service/container.

    LOG_LEVEL
        DEBUG, INFO, WARNING, ERROR, CRITICAL

    LOG_DIR
        Directory for log files.
        Default: /var/log/factoryiq

    LOG_TO_FILE
        true/false
        Default: true

Example:

    SERVICE_NAME=production-service
    LOG_LEVEL=INFO
    LOG_TO_FILE=true
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

SERVICE_NAME = os.getenv("SERVICE_NAME", "factoryiq-service")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

LOG_DIR = os.getenv("LOG_DIR", "/var/log/factoryiq")

LOG_TO_FILE = os.getenv("LOG_TO_FILE", "true").lower() in ("true", "1", "yes", "on")


# ============================================================
# Constants
# ============================================================

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================
# Convert log level
# ============================================================


def _get_log_level():
    """
    Convert LOG_LEVEL environment variable into
    Python logging level.
    """

    level = getattr(logging, LOG_LEVEL, None)

    if isinstance(level, int):
        return level

    return logging.INFO


# ============================================================
# Create file handler
# ============================================================


def _create_file_handler():
    """
    Create a rotating file handler.

    Maximum file size:
        10 MB

    Number of backup files:
        5

    Example:

        production-service.log
        production-service.log.1
        production-service.log.2
        ...
    """

    try:
        log_path = Path(LOG_DIR)

        log_path.mkdir(parents=True, exist_ok=True)

        file_path = log_path / f"{SERVICE_NAME}.log"

        handler = RotatingFileHandler(
            filename=file_path,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        handler.setLevel(_get_log_level())

        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

        handler.setFormatter(formatter)

        return handler

    except Exception as exc:
        # Never allow logging failure to crash
        # the application.

        print(f"WARNING: Could not create log file: {exc}", file=sys.stderr)

        return None


# ============================================================
# Create console handler
# ============================================================


def _create_console_handler():
    """
    Create stdout handler.

    Docker captures stdout/stderr automatically.
    """

    handler = logging.StreamHandler(sys.stdout)

    handler.setLevel(_get_log_level())

    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    handler.setFormatter(formatter)

    return handler


# ============================================================
# Logger factory
# ============================================================


def get_logger(name=None):
    """
    Return a configured logger.

    Example:

        logger = get_logger(__name__)

    """

    if name is None:
        name = SERVICE_NAME

    logger_name = f"{SERVICE_NAME}.{name}"

    logger = logging.getLogger(logger_name)

    logger.setLevel(_get_log_level())

    logger.propagate = False

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # --------------------------------------------------------
    # Console logging
    # --------------------------------------------------------

    console_handler = _create_console_handler()

    logger.addHandler(console_handler)

    # --------------------------------------------------------
    # File logging
    # --------------------------------------------------------

    if LOG_TO_FILE:
        file_handler = _create_file_handler()

        if file_handler is not None:
            logger.addHandler(file_handler)

    return logger


# ============================================================
# Default logger
# ============================================================

logger = get_logger("application")


# ============================================================
# Convenience functions
# ============================================================


def log_info(message, *args, **kwargs):
    """
    Log INFO message.
    """

    logger.info(message, *args, **kwargs)


def log_warning(message, *args, **kwargs):
    """
    Log WARNING message.
    """

    logger.warning(message, *args, **kwargs)


def log_error(message, *args, **kwargs):
    """
    Log ERROR message.
    """

    logger.error(message, *args, **kwargs)


def log_exception(message, *args, **kwargs):
    """
    Log exception with traceback.

    Use inside except block.
    """

    logger.exception(message, *args, **kwargs)


def log_debug(message, *args, **kwargs):
    """
    Log DEBUG message.
    """

    logger.debug(message, *args, **kwargs)


# ============================================================
# Application startup information
# ============================================================


def log_startup():
    """
    Log standard service startup information.
    """

    logger.info("==================================================")

    logger.info("FactoryIQ service starting")

    logger.info("Service: %s", SERVICE_NAME)

    logger.info("Log Level: %s", LOG_LEVEL)

    logger.info("Log Directory: %s", LOG_DIR)

    logger.info("File Logging: %s", LOG_TO_FILE)

    logger.info("==================================================")
