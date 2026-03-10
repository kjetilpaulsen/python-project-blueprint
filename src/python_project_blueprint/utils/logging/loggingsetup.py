from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# FIX: Change imports from "python_project_blueprint" to packagename
from python_project_blueprint.runtime.runtime import CFGLogging, AppPaths


def logging_setup(appname: str, 
                  paths: AppPaths, 
                  log: CFGLogging) -> None:
    """
    Configures the logging for the entire application

    Sets the path for all future logs to logs/trilobite.log
    """

    # Create the parent logger
    root_logger = logging.getLogger()
    root_logger.setLevel(min(log.log_level,log.console_level))

    # Remove existing handlers from logging.basicConfig
    root_logger.handlers.clear()

    # Setup of the logging format
    formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(name)s.%(funcName)s() -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
    )

    # If only logging to stderr, like in docker
    if log.log_to_stderr:
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(log.log_level)
        stderr_handler.setFormatter(formatter)
        root_logger.addHandler(stderr_handler)
        return None

    # Logging to files
    last_run_file: Path = paths.logs_dir / f"{appname}.log"
    history_file: Path = paths.logs_dir / f"{appname}_history.log"

    # History logging
    history_handler = RotatingFileHandler(
            history_file,
            maxBytes=10_000_000,
            backupCount=5,
            encoding="utf-8",
    )
    history_handler.setLevel(log.log_level)
    history_handler.setFormatter(formatter)
    root_logger.addHandler(history_handler)

    # Only last run logging
    last_run_handler = logging.FileHandler(
        last_run_file,
        mode="w",
        encoding="utf-8",
    )
    last_run_handler.setLevel(log.log_level)
    last_run_handler.setFormatter(formatter)
    root_logger.addHandler(last_run_handler)

    # If also want logging output to screen
    if log.log_to_console:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(log.console_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    return None

