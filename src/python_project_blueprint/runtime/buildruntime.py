from __future__ import annotations

from dataclasses import asdict
import logging
from importlib import metadata
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.runtime.parsedinput import RuntimeOverrides
from python_project_blueprint.runtime.runtime import (
    CFGDataBase,
    CFGDev,
    CFGLogging,
    MetaInfo,
    Runtime,
)
from python_project_blueprint.utils.paths.paths import ensure_dirs, get_app_paths


class RuntimeSettings(BaseSettings):
    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore",
    )

    #CFGDev
    dev_mode: bool = False
    dry_run: bool = False
    #CFGLogging
    log_level: int = logging.INFO
    console_level: int = logging.INFO
    console_log: bool = False
    stderr_log: bool = False
    #CFGDataBase
    db_host: str | None = None
    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_port: int | None = None

    @field_validator("log_level", "console_level", mode="before")
    @classmethod
    def validate_log_level(cls, value: object) -> int:
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            text= value.strip().upper()
            allowed = {
                "DEBUG": logging.DEBUG, 
                "INFO": logging.INFO, 
                "WARNING": logging.WARNING, 
                "ERROR": logging.ERROR, 
                "CRITICAL": logging.CRITICAL,
            }
            if text in allowed:
                return allowed[text]
            if text.isdigit():
                return int(text)
        raise ValueError(f"Unsupported log level: {value}")

def compact_context(context: dict[str, Any]) -> dict[str, Any]:
    """
    Removes keys with value None so they do not override env/.env/defaults
    """
    return {k: v for k, v in context.items() if v is not None}

def read_metadata() -> MetaInfo: 
    """
    Reads metadata from pyproject.toml and returns a dataclass with values
    """
    try:
        app_version = metadata.version(IDENTITY.dist_name)
    except metadata.PackageNotFoundError:
        app_version = "0.0.0"

    try:
        meta = metadata.metadata(IDENTITY.dist_name)
        app_description = meta.get("Summary")
    except metadata.PackageNotFoundError:
        app_description = "No description"

    return MetaInfo(
        app_name=IDENTITY.app_name,
        app_version=app_version,
        app_description=app_description,
    )


def build_runtime(rto: RuntimeOverrides) -> Runtime:
    """
    """
    #Override rule is: contex > env > .env > defaults

    clean_rto = compact_context(asdict(rto))
    settings = RuntimeSettings(**clean_rto)

    # Build Runtime dataclasses
    meta = read_metadata()

    paths = get_app_paths()
    ensure_dirs(paths, logs_dir=True)

    dev = CFGDev(
        dev_mode = settings.dev_mode,
        dry_run = settings.dry_run
    )

    log = CFGLogging(
        log_level = settings.log_level,
        console_level = settings.console_level,
        console_log = settings.console_log,
        stderr_log = settings.stderr_log,
    )

    db = CFGDataBase(
        db_host = settings.db_host or "/run/postgresql",
        db_dbname = settings.db_name or meta.app_name.replace("-","_"),
        db_user = settings.db_user,
        db_password = settings.db_password,
        db_port = settings.db_port or 5432,
    )

    return Runtime(
        meta=meta,
        paths=paths,
        dev=dev,
        log=log,
        db=db,
    )
