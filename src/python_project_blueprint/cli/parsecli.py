from __future__ import annotations

import argparse
import sys

def parse_cli(APPNAME: str) -> dict:
    """
    Resolves argv and returns the arguments passed as a dict

    To add more args:
    - parser.add_argument()
    - Add to return dict
    """
    parser = argparse.ArgumentParser(prog = APPNAME)

    parser.add_argument("--dev-mode", action=argparse.BooleanOptionalAction, default=None, help="Enable developer conviniences")
    parser.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=None, help="Do not write to DB")

    parser.add_argument("--log-level", type=str, help="Set the general logging level for the app")
    parser.add_argument("--console-level", type=str, help="Set the logging level consolelogging")
    parser.add_argument("--console-log", action=argparse.BooleanOptionalAction, default=None, help="Enable logging to console")
    parser.add_argument("--stderr-log", action=argparse.BooleanOptionalAction, default=None, help="Enable logging to stder")

    parser.add_argument("--db-host", default=None)
    parser.add_argument("--db-name", default=None)
    parser.add_argument("--db-username", default=None)
    parser.add_argument("--db-password", default=None)
    parser.add_argument("--db-port", type=int, default=None)

    #Commands
    parser.add_argument("--version", action="store_true", help="Displays the current version of the program")

    args = parser.parse_args(sys.argv[1:])

    return {
        "dev_mode": args.dev_mode,
        "dry_run": args.dry_run,
        "log_level": args.log_level,
        "console_level": args.console_level,
        "console_log": args.console_log,
        "stderr_log": args.stderr_log,
        "db_host": args.db_host,
        "db_name": args.db_name,
        "db_username": args.db_username,
        "db_password": args.db_password,
        "db_port": args.db_port,

        "version": args.version,
    }
