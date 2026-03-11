from __future__ import annotations

import logging
import sys

# FIX: Change imports from "python_project_blueprint" to packagename
from python_project_blueprint.cli.clieventhandler import CliEventHandler
from python_project_blueprint.commands.buildcommands import build_commands
from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.utils.logging.loggingsetup import logging_basic_setup, logging_setup
from python_project_blueprint.runtime.buildruntime import build_runtime
from python_project_blueprint.cli.parsecli import parse_cli
from python_project_blueprint.app import App
from python_project_blueprint.utils.logging.logruntime import log_runtime

def main() -> int:
    """
    Main entrypoint for CLI
    """

    # Setup basic logging
    logging_basic_setup()
    logger = logging.getLogger(IDENTITY.logger_name)
    logger.info("Basic logging started")

    # Try to start program
    try:
        parsed_input = parse_cli()

        commands = build_commands(parsed_input.commands)
        rt = build_runtime(parsed_input.overrides)

        logging_setup(IDENTITY.logger_name,
                      rt.paths,
                      rt.log)
        log_runtime(rt)

        app = App(rt.meta, rt.dev, rt.db, rt.paths)
        evt_handler = CliEventHandler()

        for evt in app.run(commands):
            evt_handler.handle(evt)

    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        sys.exit(130)
    except Exception:
        logger.exception("---FATAL ERROR---")
        sys.exit(1)
    sys.exit(0)

