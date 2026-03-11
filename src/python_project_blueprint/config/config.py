from __future__ import annotations

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
LOG_LEVEL=info

# Level of logging that happens in console, CONSOLE_LOG must be true
CONSOLE_LEVEL=info

# Log to files, specified by XDG-paths
FILE_LOG=false

# Log to console
CONSOLE_LOG=false

# Log to stderr
STDERR_LOG=false

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
    Builds the .conf file in the XDG resolved config directory. Take care that
    if this file already exists, it will be overritten. Meaning this command 
    can be called in order to reset a broken .conf file.

    @Params
    - paths: AppPaths
    """
    config_path = paths.config_dir / f"{IDENTITY.logger_name}.conf"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with config_path.open("w", encoding="utf-8") as f:
        f.write(CONFIG_TEMPLATE)

