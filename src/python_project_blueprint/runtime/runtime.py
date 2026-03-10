from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

# Immutables
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
    dev: bool = False
    dry_run: bool = False

@dataclass(frozen=True)
class CFGLogging:
    log_level: int = logging.INFO
    console_level: int = logging.INFO
    log_to_console: bool | None = False
    log_to_stderr: bool = False

@dataclass(frozen=True)
class CFGDataBase:
    dbname: str = "myapp"
    host: str  = "/run/postgresql"
    user: str | None = None
    port: int = 5432

# Mutables
@dataclass
class CmdFirstCommand:
    run: bool = False

# Consolidation
@dataclass(frozen=True)
class Runtime:
    paths: AppPaths
    dev: CFGDev
    log: CFGLogging
    db: CFGDataBase

    cmds: list = [
    CmdFirstCommand,
    ]

