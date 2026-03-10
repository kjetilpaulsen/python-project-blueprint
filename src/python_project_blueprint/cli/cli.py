from __future__ import annotations

import logging
import sys
from typing import NoReturn
# FIX: Change imports from "python_project_blueprint" to packagename
from python_project_blueprint.utils.logging.loggingsetup import logging_setup
from python_project_blueprint.runtime.buildruntime import build_runtime
from python_project_blueprint.cli.parsecli import parse_cli
from python_project_blueprint.app import App
from python_project_blueprint.utils.logging.logruntime import log_runtime

#parse args/json into a dataclass (None  or Value)
#pass that dataclass into build_context(dc)
#build_context builds context dataclass, which consists of cfg datalcass, cmd
#dataclass(or list). This is done by first loading the defaults, then override with envs
#then override with the dc passed.
#When this is returned, the responding configs are sent where they are needed:
#e.g. to logger_setup(context.logging)
#app = App(context.cfg) is called
#app.run(context.commands) is called
#-------------------
#Create dict from args, api also creates dict. pass those to build context/runtime
#Create load_env function in env, it returns a dict. make sure to create resolves for different values
#Combine the two, and use the combination to create the runtime 


def main() -> NoReturn:
    """
    Main entrypoint for CLI:
    - Calls build_runtime
    - Calls logging_setup
    - Calls App.__init__
    - Calls app.run
    """
    # FIX: Change appname
    APPNAME = "python-project-blueprint"

    # Setup basic logging
    #-------------------------------------------------------------------------#
    logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger(APPNAME)

    # Try to start program
    #-------------------------------------------------------------------------#
    try:
        rt = build_runtime(APPNAME, parse_cli(APPNAME))
        logging_setup(APPNAME,
                      rt.paths,
                      rt.log)

        log_runtime(rt)
        app = App(rt.meta, rt.dev, rt.db, rt.paths)
        app.run(rt.cmds)
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        sys.exit(130)
    except Exception:
        # Any uncaught exceptions are logged before dying
        logger.exception("---FATAL ERROR---")
        sys.exit(1)
    #-------------------------------------------------------------------------#
    sys.exit(0)

