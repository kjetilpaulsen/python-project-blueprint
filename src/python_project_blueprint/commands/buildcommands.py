from __future__ import annotations

from python_project_blueprint.commands.commands import Command, DisplayVersion
from python_project_blueprint.runtime.parsedinput import FrontendCommandInput

def build_commands(cmd_inputs: tuple[FrontendCommandInput, ...]) -> tuple[Command, ...]:
    commands: list[Command] = []

    for item in cmd_inputs:
        if item.name == "version":
            uppercase = bool(item.options.get("uppercase", False))
            commands.append(DisplayVersion(uppercase=uppercase))
            continue

        raise ValueError(f"Unsupported command input: {item.name}")

    return tuple(commands)

