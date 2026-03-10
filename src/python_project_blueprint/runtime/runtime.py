from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

# Immutables
@dataclass(frozen=True)
class MetaInfo:
    app_name: str
    app_version: str
    app_description: str

@dataclass(frozen=True)
class AppPaths:
    data_dir: Path
    state_dir: Path
    cache_dir: Path
    tmp_dir: Path
    config_dir: Path

    #Add alternative subfolders like so
    @property
    def logs_dir(self) -> Path:
        return self.state_dir / "logs"

@dataclass(frozen=True)
class CFGDev:
    dev_mode: bool = False
    dry_run: bool = False

@dataclass(frozen=True)
class CFGLogging:
    log_level: int = logging.INFO
    console_level: int = logging.INFO
    console_log: bool = False
    stderr_log: bool = False

@dataclass(frozen=True)
class CFGDataBase:
    db_host: str | None = None
    db_dbname: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_port: int | None = None

# Mutables
@dataclass
class CmdDisplayVersion:
    run: bool = False

# Consolidation
@dataclass(frozen=True)
class Runtime:
    meta: MetaInfo
    paths: AppPaths
    dev: CFGDev
    log: CFGLogging
    db: CFGDataBase

    cmds: tuple[
        CmdDisplayVersion,
    ]

