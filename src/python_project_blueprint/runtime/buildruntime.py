from __future__ import annotations

from dataclasses import asdict
import logging
from importlib import metadata
import pathlib
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# FIX: change project name for imports
from python_project_blueprint.config.config import build_config_file
from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.runtime.parsedinput import RuntimeOverrides
from python_project_blueprint.runtime.runtime import (
    CFGDataBase,
    CFGDev,
    CFGLogging,
    CFGMisc,
    MetaInfo,
    Runtime,
)
from python_project_blueprint.utils.paths.paths import ensure_dirs, ensure_optional_dirs, get_app_paths
from python_project_blueprint.utils.utils import resolve_version

logger = logging.getLogger(__name__)

def resolve_env_file() -> str | None:
    """
    Resolve the configuration file path used by `RuntimeSettings`.

    The function first checks for a `.env` file in the current working
    directory. If that file does not exist, it checks for an application
    config file in the XDG config directory. If neither file exists,
    `None` is returned.

    Returns:
        str | None: The path to the `.env` or `.conf` file to use, or
        `None` if no configuration file was found.
    """
    cwd_env = pathlib.Path.cwd() / ".env"
    if cwd_env.exists():
        return str(cwd_env)
    xdg_env = get_app_paths().config_dir / (IDENTITY.logger_name + ".conf")
    if xdg_env.exists():
        return str(xdg_env)
    return None

class RuntimeSettings(BaseSettings):
    """
    Application runtime settings resolved from overrides, environment
    variables, config files, and defaults.

    The settings model defines the precedence-controlled runtime
    configuration used to construct the application's runtime dataclasses.
    The actual precedence is determined by how values are passed into the
    model together with `BaseSettings` resolution behavior.

    Attributes:
        dev_mode: Enable developer-oriented behavior.
        dry_run: Disable write operations and other side effects.
        log_level: Base logging level, typically used for file logging.
        console_level: Logging level for console output.
        stderr_level: Logging level for stderr output.
        file_log: Enable file-based logging.
        console_log: Enable console logging.
        stderr_log: Enable stderr logging.
        db_host: Database host or socket path.
        db_name: Database name.
        db_user: Database username.
        db_password: Database password.
        db_port: Database port.
        build_config: Whether to create a config file in the XDG config
            directory.
    """
    model_config = SettingsConfigDict(
            env_file=resolve_env_file(),
            env_file_encoding="utf-8",
            extra="ignore",
    )

    #CFGDev
    dev_mode: bool = False
    dry_run: bool = False
    #CFGLogging
    log_level: int = logging.DEBUG
    console_level: int = logging.INFO
    stderr_level: int = logging.WARNING
    file_log: bool = False
    console_log: bool = False
    stderr_log: bool = True
    #CFGDataBase
    db_host: str | None = None
    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_port: int | None = None
    #CFGMisc
    build_config: bool | None = None

    @field_validator("log_level", "console_level", "stderr_level", mode="before")
    @classmethod
    def validate_log_level(cls, value: object) -> int:
        """
        Validate and normalize a logging level value.

        The validator accepts either an integer logging level or a string
        representation such as `"DEBUG"`, `"INFO"`, `"WARNING"`,
        `"ERROR"`, or `"CRITICAL"`. Numeric strings are also accepted.

        Args:
            value: The raw logging level value to validate.

        Returns:
            int: A normalized integer logging level.

        Raises:
            ValueError: If the value is not a supported logging level.
        """
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


def read_metadata() -> MetaInfo: 
    """
    Read application metadata and return it as a `MetaInfo` object.

    The function resolves the application version and description from
    installed package metadata. If metadata cannot be found, fallback
    strings are used instead.

    Returns:
        MetaInfo: A metadata object containing the application name,
        version, and description.
    """
    try:
        app_version = resolve_version()
    except metadata.PackageNotFoundError as e:
        app_version = f"Failed to find version - {e}"

    try:
        meta = metadata.metadata(IDENTITY.dist_name)
        app_description = str(meta.get("Summary"))
    except metadata.PackageNotFoundError as e:
        app_description = f"Failed to find description - {e}"

    return MetaInfo(
        app_name=IDENTITY.app_name,
        app_version=app_version,
        app_description=app_description)

def _compact_context(context: dict[str, Any]) -> dict[str, Any]:
    """
    Remove keys whose values are `None`.

    This is used so unset override values do not replace values resolved
    from environment variables, config files, or defaults.

    Args:
        context: A mapping of configuration keys to values.

    Returns:
        dict[str, Any]: A new dictionary containing only keys whose values
        are not `None`.
    """
    return {k: v for k, v in context.items() if v is not None}

def build_runtime(rto: RuntimeOverrides | None = None) -> Runtime:
    """
    Build the full application runtime from resolved configuration.

    The runtime is assembled from metadata, XDG paths, optional override
    values, environment/config settings, and defaults. The resulting
    `Runtime` object contains the grouped dataclasses used by the rest of
    the application.

    Configuration precedence is:

        overrides > environment > `.env` / `.conf` > defaults

    Args:
        rto: Optional runtime overrides, typically provided by the CLI.
            If omitted, runtime settings are resolved entirely from
            environment/config/default sources.

    Returns:
        Runtime: The fully constructed runtime-settings object.
    """
    logger.info("Building runtime ..")

    meta = read_metadata()

    paths = get_app_paths()
    ensure_dirs(paths)

    clean_rto = _compact_context(asdict(rto)) if rto is not None else {}
    settings = RuntimeSettings(**clean_rto)

    if settings.build_config:
        logger.info("Building config file ..")
        build_config_file(paths)

    ensure_optional_dirs(paths, logs_dir=settings.file_log)

    dev = CFGDev(
        dev_mode = settings.dev_mode,
        dry_run = settings.dry_run
    )

    log = CFGLogging(
        log_level = settings.log_level,
        console_level = settings.console_level,
        file_log = settings.file_log,
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
    misc=CFGMisc(
        build_config = settings.build_config,
    )

    return Runtime(
        meta=meta,
        paths=paths,
        dev=dev,
        log=log,
        db=db,
        misc=misc,
    )
