from __future__ import annotations
import logging

from python_project_blueprint.commands.commands import Command, DisplayVersion
from python_project_blueprint.runtime.parsedinput import FrontendCommandInput

logger = logging.getLogger(__name__)

def build_commands(cmd_inputs: tuple[FrontendCommandInput, ...]) -> tuple[Command, ...]:

    logger.info("Building commands ..")

    commands: list[Command] = []

    for item in cmd_inputs:
        if item.name == "version":
            uppercase = bool(item.options.get("uppercase", False))
            commands.append(DisplayVersion(uppercase=uppercase))
            continue

        raise ValueError(f"Unsupported command input: {item.name}")

    return tuple(commands)

