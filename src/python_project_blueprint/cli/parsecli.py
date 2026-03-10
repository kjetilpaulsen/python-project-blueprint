from __future__ import annotations

import argparse
import sys

def parse_cli(APPNAME: str) -> dict:
    """
    Resolves argv and returns the arguments passed as a dict
    Keep in mind that if there are default values set in args, it will override
    envs, as well as defaults. Meaning, dont set default values for args
    """
    p = argparse.ArgumentParser(prog = APPNAME)
    p.add_argument("--dev", action=argparse.BooleanOptionalAction, default=None, help="Enable developer conviniences")
    p.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=None, help="Do not write to DB")

    p.add_argument("--log-level", type=str, help="Set the general logging level for the app")
    p.add_argument("--console-level", type=str, help="Set the logging level consolelogging")
    p.add_argument("--console-log", action=argparse.BooleanOptionalAction, default=None, help="Enable logging to console")
    p.add_argument("--stderr-log", action=argparse.BooleanOptionalAction, default=None, help="Enable logging to stder")

    args = p.parse_args(sys.argv[1:])
    return vars(args)
