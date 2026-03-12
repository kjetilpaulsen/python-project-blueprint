from __future__ import annotations

import argparse
import logging

from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.runtime.parsedinput import FrontendCommandInput, CliParsedInput, RuntimeOverrides

logger = logging.getLogger(__name__)

def cli_parser(argv: list[str] | None = None) -> CliParsedInput:
    """
    Resolves argv and returns the arguments passed as a dict

    To add more args:
    - parser.add_argument()
    - Add to return dict
    """

    logger.info("Parsing argv ..")

    parser = argparse.ArgumentParser(prog = IDENTITY.app_name)

    parser.add_argument("--dev-mode", action=argparse.BooleanOptionalAction, default=None, help="Enable developer conviniences")
    parser.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=None, help="Do not write to DB")
    parser.add_argument("--build-config", action=argparse.BooleanOptionalAction, default=None, help="Build a .conf file at XDG config path")

    parser.add_argument("--log-level", type=str, default=None, help="Set the general logging level for the app")
    parser.add_argument("--console-level", type=str, default=None, help="Set the logging level consolelogging")
    parser.add_argument("--file-log", action=argparse.BooleanOptionalAction, default=None, help="Enable logging to files")
    parser.add_argument("--console-log", action=argparse.BooleanOptionalAction, default=None, help="Enable logging to console")
    parser.add_argument("--stderr-log", action=argparse.BooleanOptionalAction, default=None, help="Enable logging to stder")

    parser.add_argument("--db-host", default=None)
    parser.add_argument("--db-name", default=None)
    parser.add_argument("--db-user", default=None)
    parser.add_argument("--db-password", default=None)
    parser.add_argument("--db-port", type=int, default=None)

    # Subparsers
    subparses = parser.add_subparsers(dest="command")

    # Version
    version_parser = subparses.add_parser("version", help="Display the current version")
    version_parser.add_argument("--uppercase", action="store_true", default=False, help="Displays the version in uppercase letters")

    # Parse them

    args = parser.parse_args(argv)

    overrides = RuntimeOverrides(
        dev_mode=args.dev_mode,
        dry_run=args.dry_run,
        build_config=args.build_config,
        log_level=args.log_level,
        console_level=args.console_level,
        file_log=args.file_log,
        console_log=args.console_log,
        stderr_log=args.stderr_log,
        db_host=args.db_host,
        db_name=args.db_name,
        db_user=args.db_user,
        db_password=args.db_password,
        db_port=args.db_port,
    )

    commands: list[FrontendCommandInput] = []
    if args.command == "version":
        commands.append(
            FrontendCommandInput(
                name="version",
                options={
                    "uppercase": args.uppercase,
                },
            )
        )
    return CliParsedInput(
        overrides=overrides,
        commands=tuple(commands),
    )
