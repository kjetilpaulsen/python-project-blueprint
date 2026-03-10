"""
Creates baseline directories for data, state, cache, tmp and config. Docker
overrides XDG values.

---To create more directories---

AppPaths in runtime.py:
    - Add @property
ensure_dirs in paths.py:
    - Add paths.*.mkdir()

"""

from __future__ import annotations

import os
from pathlib import Path

from python_project_blueprint.runtime.runtime import AppPaths


def _xdg_home(var: str, fallback: Path) -> Path:
    """
    Creates a path from the env string

    @Params
    - var: str : env string name
    - fallback: Path : fallback path

    @Returns
    - Path ( env if it exists, fallback if not)
    """
    v = os.getenv(var)
    return Path(v) if v and v.strip() else fallback

def get_app_paths(app_name: str) -> AppPaths:
    """
    XDG-based paths.

    Local (default):
        data: ~/.local/share/<app_name>
        state: ~/.local/state/<app_name>
        cache: ~/.cache/<app_name>
        tmp: ~/.cache/<app_nam>/tmp
        config: ~/.config/<app_name>
    
    Docker:
        Sets XDG_*_HOME to /data, /state, /cache, /config -> /data/<app_name> ..

    @Params
    - app_name : str : the name of the application

    @Returns
    - AppPaths : dataclass : containing the paths
    """
    app_name = app_name.strip()
    if not app_name:
        raise ValueError("app_name must be non-empty")

    home = Path.home()

    data_home = _xdg_home("XDG_DATA_HOME", home / ".local" / "share")
    state_home = _xdg_home("XDG_STATE_HOME", home / ".local" / "state")
    cache_home = _xdg_home("XDG_CACHE_HOME", home / ".cache")
    config_home = _xdg_home("XDG_CONFIG_HOME", home / ".config")

    data_dir = data_home / app_name
    state_dir = state_home / app_name
    cache_dir = cache_home / app_name
    config_dir = config_home / app_name

    tmp_dir = cache_dir / "tmp"

    return AppPaths(data_dir, state_dir, cache_dir, tmp_dir, config_dir)

def ensure_dirs(paths: AppPaths, 
                logs_dir: bool = False,
                ) -> None:
    """
    Creates the directories if they don't already exist

    @Params
    - paths: AppPaths

    @Returns
    - None
    """
    for p in (paths.data_dir, paths.state_dir, paths.cache_dir, paths.tmp_dir, paths.config_dir):
        p.mkdir(parents=True, exist_ok=True)
    # If you have added more to AppPaths, you creates those dirs here, remember
    # to also add them to the params of ensure_dirs
    if logs_dir:
        paths.logs_dir.mkdir(parents=True, exist_ok = True)
