from __future__ import annotations
from collections.abc import Iterable, Iterator, Sequence
from typing import Any
import logging

from python_project_blueprint.commands.commands import Command, DisplayVersion
from python_project_blueprint.events.events import Event
from python_project_blueprint.handlers.displayversionhandler import DisplayVersionHandler
from python_project_blueprint.runtime.runtime import AppPaths, CFGDataBase, CFGDev, MetaInfo


logger = logging.getLogger(__name__)

class App:
    """
    The back-engine of the program. Spawns and owns most services. Contains
    the run(cmd) method that produces the results.
    """
    def __init__(self, meta: MetaInfo, dev: CFGDev, db: CFGDataBase, paths: AppPaths) -> None:
        logger.debug("Start ..")
        self.meta = meta
        self.dev = dev
        self.db = db
        self.paths = paths

        # Start services..

    def run(self, cmds: Sequence[Command]) -> Iterator[Event]:
        """
        The method takes in a sequence of commands, calls _handle_command for
        each command, and then yields back Events produced by the command

        @Params
        - cmds: Sequence[Command]

        @Returns
        - yields Iterator[Event]
        """
        for cmd in cmds:
            yield from self._handle_command(cmd)

    def _handle_command(self, cmd: Command) -> Iterator[Event]:
        """
        Checks which commands was given, and then calls the appropriate and 
        corresponding classes.

        @Params
        - cmd: Command

        @Returns
        - yields Iterator[Event]
        """
        if isinstance(cmd, DisplayVersion):
            cmd_handler = DisplayVersionHandler(self.meta)
            yield from cmd_handler.handle()
            return
        raise ValueError(f"Unsupported command: {type(cmd).__name__}")
