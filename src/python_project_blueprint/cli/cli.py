from __future__ import annotations

import logging
import sys
from typing import NoReturn

# FIX: Change imports from "python_project_blueprint" to packagename
from python_project_blueprint.cli.clieventhandler import CliEventHandler
from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.utils.logging.loggingsetup import logging_setup
from python_project_blueprint.runtime.buildruntime import build_runtime
from python_project_blueprint.cli.parsecli import parse_cli
from python_project_blueprint.app import App
from python_project_blueprint.utils.logging.logruntime import log_runtime

def main() -> NoReturn:
    """
    Main entrypoint for CLI:
    """

    # Setup basic logging
    logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger(IDENTITY.app_name)

    # Try to start program
    try:
        pi = parse_cli()
        rt = build_runtime(pi.overrides)
        logging_setup(IDENTITY.logger_name,
                      rt.paths,
                      rt.log)
        log_runtime(rt)
        app = App(rt.meta, rt.dev, rt.db, rt.paths)
        evt_handler = CliEventHandler()
        for evt in app.run(pi.commands):
            evt_handler.handle(evt)
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        sys.exit(130)
    except Exception:
        logger.exception("---FATAL ERROR---")
        sys.exit(1)
    sys.exit(0)

