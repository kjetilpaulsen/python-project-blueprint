from __future__ import annotations

# FIX: change project name for imports
from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.runtime.runtime import AppPaths

CONFIG_TEMPLATE = """########
# Misc #
########

# Enable developer conviniences
DEV_MODE=false

# Run without writing to DB
DRY_RUN=false

# Build new version of config file at XDG-Config path, overrites current file
BUILD_CONFIG=false

###########
# Logging #
###########

# Level of general logging
LOG_LEVEL=debug

# Level of logging that happens in console, CONSOLE_LOG must be true
CONSOLE_LEVEL=info

# Level og logging that happens to stderr, STDERR_LOG must be true
STDERR_LEVEL=warning

# Log to files, specified by XDG-paths
FILE_LOG=false

# Log to console
CONSOLE_LOG=false

# Log to stderr
STDERR_LOG=true

##################################
# PostgreSQL connection settings #
##################################

# Leave empty for local socket connection
DB_HOST=

# Default suggestion: use the application name
DB_NAME=

# Leave empty to use system user
DB_USER=

# Leave password empty for peer/local auth
DB_PASSWORD=

# Default port
DB_PORT=5432
"""

def build_config_file(paths: AppPaths) -> None:
    """
    Create or overwrite the application's configuration file.

    This function writes a default configuration template to the XDG
    configuration directory resolved by `AppPaths`. If the configuration
    file already exists, it will be overwritten. This allows the command
    to be used to regenerate or reset a broken configuration file.

    The configuration file is written using the application's package
    name as the base filename.

    Args:
        paths: Application path container used to resolve the XDG
            configuration directory where the configuration file
            should be created.

    Returns:
        None
    """
    config_path = paths.config_dir / f"{IDENTITY.package_name}.conf"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with config_path.open("w", encoding="utf-8") as f:
        f.write(CONFIG_TEMPLATE)

