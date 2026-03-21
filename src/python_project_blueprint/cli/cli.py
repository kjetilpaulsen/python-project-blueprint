from __future__ import annotations

import logging

# FIX: change project name for imports
from python_project_blueprint.cli.clieventhandler import CliEventHandler
from python_project_blueprint.commands.buildcommands import build_commands
from python_project_blueprint.commands.commands import Command
from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.runtime.runtime import Runtime
from python_project_blueprint.utils.logging.setuplogging import setup_logging
from python_project_blueprint.runtime.buildruntime import build_runtime
from python_project_blueprint.cli.cliparser import cli_parser
from python_project_blueprint.app import App
from python_project_blueprint.runtime.logruntime import log_runtime

logger = logging.getLogger(__name__)

def cli(argv: list[str] | None = None) -> int:
    """
    Execute the command-line interface entrypoint.

    This function parses CLI arguments, builds the application runtime,
    configures logging, and executes the requested commands through the
    application engine.

    The CLI follows this execution flow:

        1. Parse command-line arguments into structured command inputs.
        2. Convert command inputs into executable command objects.
        3. Build the runtime configuration (paths, logging, database, etc.).
        4. Configure logging according to runtime settings.
        5. Run the application command pipeline and handle emitted events.

    Args:
        argv: Optional list of CLI arguments. If `None`, arguments are read
            from `sys.argv` by the CLI parser. This parameter is primarily
            useful for testing or programmatic invocation.

    Returns:
        int: Process exit code.

            - `0` if execution completed successfully.
            - `130` if execution was interrupted by the user (Ctrl+C).
            - `1` if an unexpected fatal error occurred.
    """
    logger.info("--STARTING CLI--")
    try:
        frontendinputcommands, overrides = cli_parser(argv)

        commands: list[Command] = [build_commands(cmd) for cmd in frontendinputcommands]
        runtime: Runtime = build_runtime(overrides)

        setup_logging(IDENTITY.logger_name,
                      runtime.paths,
                      runtime.log)
        log_runtime(runtime)

        app = App(runtime.meta, runtime.dev, runtime.db, runtime.paths)
        evt_handler = CliEventHandler()

        while commands:
            cmd, *commands = commands
            for evt in app.run(cmd):
                ret = evt_handler.handle(evt)
                if isinstance(ret, Command):
                    commands.append(ret)

    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        return 130
    except Exception:
        logger.exception("---FATAL ERROR---")
        return 1
    return 0

