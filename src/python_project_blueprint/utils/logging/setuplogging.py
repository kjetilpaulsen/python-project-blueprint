from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# FIX: Change imports from "python_project_blueprint" to packagename
from python_project_blueprint.runtime.runtime import CFGLogging, AppPaths

_LOGGING_INITIALIZED = False

class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level: int) -> None:
        super().__init__()
        self.max_level = max_level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno <= self.max_level

def setup_basic_logging() -> None:
    """
    Sets up very basic level of logging to stderr before config, paths, logging
    is configured.
    """
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True,
    )

def _configure_logging(appname: str, 
                  paths: AppPaths, 
                  log: CFGLogging) -> None:
    """
    Configures the logging for the entire application

    Sets the path for all future logs to logs/trilobite.log
    """
    logger = logging.getLogger(__name__)
    logger.info("Configuring logging ..")
    # Create the parent logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Remove existing handlers from logging.basicConfig
    root_logger.handlers.clear()

    # Setup of the logging format
    file_formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(name)s.%(funcName)s() -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Setup of the logging format
    console_formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Setup of the logging format
    stderr_formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
    )

    # If only logging to stderr
    if log.stderr_log:
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(log.stderr_level)
        stderr_handler.setFormatter(stderr_formatter)
        root_logger.addHandler(stderr_handler)

    # Logging to files
    if log.file_log:
        last_run_file: Path = paths.logs_dir / f"{appname}.log"
        history_file: Path = paths.logs_dir / f"{appname}_history.log"

        # History logging
        try:
            history_handler = RotatingFileHandler(
                    history_file,
                    maxBytes=10_000_000,
                    backupCount=5,
                    encoding="utf-8",
            )
            history_handler.setLevel(log.log_level)
            history_handler.setFormatter(file_formatter)
            root_logger.addHandler(history_handler)
        except OSError:
            logger.exception("Failed to configure rotating file handler logging for %s", history_file)

        # Only last run logging
        try:
            last_run_handler = logging.FileHandler(
                last_run_file,
                mode="w",
                encoding="utf-8",
            )
            last_run_handler.setLevel(log.log_level)
            last_run_handler.setFormatter(file_formatter)
            root_logger.addHandler(last_run_handler)
        except OSError:
            logger.exception("Failed to configure file handler logging for %s", last_run_file)

    # If also want logging output to screen
    if log.console_log:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(log.console_level)
        if log.stderr_log:
            console_handler.addFilter(MaxLevelFilter(log.stderr_level))
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    return None

def setup_logging(appname: str, paths: AppPaths, log: CFGLogging) -> None:
    """
    CLI-style logging setup: always rebuild the process logging config.
    """
    global _LOGGING_INITIALIZED
    _configure_logging(appname, paths, log)
    _LOGGING_INITIALIZED = True

def ensure_setup_logging(appname: str, paths: AppPaths, log: CFGLogging) -> None:
    """
    API-style logging setup: configure it once per process.
    """
    global _LOGGING_INITIALIZED
    if _LOGGING_INITIALIZED:
        return
    _configure_logging(appname, paths, log)
    _LOGGING_INITIALIZED = True
