from __future__ import annotations

import logging
import sys

# FIX: Change imports from "python_project_blueprint" to packagename
from python_project_blueprint.cli.clieventhandler import CliEventHandler
from python_project_blueprint.commands.buildcommands import build_commands
from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.utils.logging.loggingsetup import logging_setup
from python_project_blueprint.runtime.buildruntime import build_runtime
from python_project_blueprint.cli.cliparser import cli_parser
from python_project_blueprint.app import App
from python_project_blueprint.utils.logging.logruntime import log_runtime

def cli(argv: list[str] | None = None) -> int:
    """
    Main entrypoint for CLI
    """
    logger = logging.getLogger(IDENTITY.logger_name)
    logger.info("Starting CLI entrypoint")
    try:
        parsed_input = cli_parser(argv)

        commands = build_commands(parsed_input.commands)
        runtime = build_runtime(parsed_input.overrides)

        logger.info("Setting up logger ..")
        logging_setup(IDENTITY.logger_name,
                      runtime.paths,
                      runtime.log)
        log_runtime(runtime)

        app = App(runtime.meta, runtime.dev, runtime.db, runtime.paths)
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

