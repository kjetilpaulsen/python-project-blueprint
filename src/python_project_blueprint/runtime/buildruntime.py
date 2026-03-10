from __future__ import annotations

import logging
import argparse
import os
import sys
from typing import NoReturn

from dev_standards.logging.loggingsetup import logging_setup
from dev_standards.utils.paths.paths import ensure_dirs, get_app_paths
from dev_standards.runtime.runtime import CFGDataBase, CFGDev, CFGLogging, CmdFirstCommand, Runtime
from dev_standards.cli.parsecli import parse_cli
from dev_standards.runtime.envs.loadenvs import load_envs

def build_runtime(APPNAME: str, context: dict) -> Runtime:
    """
    """
    #Context is a dict containing userspesified settings
    #it comes in by default from either entrypoint

    #Now we load the envs, and return them as a dict here
    context_envs = load_envs()

    #Now we resolve the two context dicts, context override context_env

    #-------------------------------------------------------------------------#
    #Helper functions
    def _decide(arg, env, default) -> bool:
        if arg is not None:
            return arg
        if env is not None:
            return env
        return default

    def _resolve_env(name: str) -> bool | None:
        v = os.getenv(name)
        return None if v is None else v.lower() == "true"

    def _resolve_log_level(level: str) -> int:
        if level.lower() == "debug":
            return logging.DEBUG
        if level.lower() == "info":
            return logging.INFO
        if level.lower() == "warning":
            return logging.WARNING
        if level.lower() == "error":
            return logging.ERROR
        return logging.INFO
    #-------------------------------------------------------------------------#
    #Setup paths
    paths = get_app_paths(APPNAME)
    ensure_dirs(paths)
    #-------------------------------------------------------------------------#
    # Building Runtime parts
    dev = CFGDev(
        dev = _decide(args.dev, _resolve_env("DEV"), CFGDev.dev),
        dry_run = _decide(args.dry_run, _resolve_env("DRYRUN"), CFGDev.dry_run),
    )
    log = CFGLogging(
        log_level = _decide(_resolve_log_level(args.log_level), None, CFGLogging.log_level), # must add fix for env level set
        console_level = _decide(_resolve_log_level(args.console_level), None, CFGLogging.console_level), # must add fix for env level set
        log_to_console = _decide(args.console_log, _resolve_env("LOGTOCONSOLE"), CFGLogging.log_to_console),
        log_to_stderr = _decide(args.stderr_log, _resolve_env("LOGTOSTDERR"), CFGLogging.log_to_stderr),
    )
    db = CFGDataBase()
    commands = [
        CmdFirstCommand(),
    ]
    #-------------------------------------------------------------------------#
    #Return
    return Runtime(
        paths=paths,
        dev=dev,
        log=log,
        db=db,
        cmds=commands,
    )
