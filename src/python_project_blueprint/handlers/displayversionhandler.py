from __future__ import annotations
import logging
from typing import Any, Iterator

from python_project_blueprint.commands.commands import Command
from python_project_blueprint.events.events import Event, EvtResult
from python_project_blueprint.handlers.commandhandler import CommandHandler
from python_project_blueprint.runtime.runtime import MetaInfo

logger = logging.getLogger(__name__)

class DisplayVersionHandler(CommandHandler):
    def __init__(self, cmd: Command, meta: MetaInfo):
        self.cmd = cmd
        self.meta = meta

    def handle(self) -> Iterator[Event]:
        """
        Similar entrypoint for every handler. This method starts the 
        computations. And it yields back different events based on the type of 
        Command it corresponds to. This docstring is a generic string for all 
        handler.handle() commands.

        This method simply calls yield from some relevant method. The relevant
        methods can produce Events in the following manner:

        Produce e.g. EvtResult:
        yield EvtResult()

        Progress events followed by e.g. EvtResult:
        total = x
        for i in range(x):
            yield EvtProgress()
        yield EvtResult()

        @Returns
        - yields Events
        """
        yield from self.display_version()

    def display_version(self) -> Iterator[Event]:
        """
        Produces an EvtResult containing the current version of the program.

        @Returns
        - yields EvtResult
        """
        version = f"v{self.meta.app_version}"
        if self.cmd.uppercase:
            version = version.upper()
        yield EvtResult(
            command_name="DisplayVersion",
            payload={"version": version},
            )
