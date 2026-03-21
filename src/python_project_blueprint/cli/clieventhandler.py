from __future__ import annotations

import logging
from typing import Callable, Iterator
from typing_extensions import Any

# FIX: change project name for imports
from python_project_blueprint.commands.commands import CmdDisplayVersion, Command
from python_project_blueprint.events.events import Event, EvtError, EvtLog, EvtProgress, EvtRequest, EvtResult

logger = logging.getLogger(__name__)

class CliEventHandler:
    """
    Handle application events for the CLI frontend.

    The `CliEventHandler` receives events produced by the application
    execution pipeline and converts them into CLI-visible output such
    as log messages, progress indicators, or printed results.

    Each event type corresponds to a specific frontend behavior. This
    keeps the CLI presentation layer separated from the core application
    logic.

    Event types currently handled include:

        - `EvtLog`: informational log messages
        - `EvtProgress`: progress updates for long-running tasks
        - `EvtError`: error reporting
        - `EvtResult`: command execution results

    Unrecognized event types are logged as warnings.
    FIX: update docstring
    """
    def __init__(self) -> None:
        self._events: dict[type[Event], Callable] ={
            EvtLog: lambda evt: self._handle_evtlog(evt),
            EvtProgress: lambda evt: self._handle_evtprogress(evt),
            EvtError: lambda evt: self._handle_evterror(evt),
            EvtResult: lambda evt: self._handle_evtresult(evt),
            EvtRequest: lambda evt: self._handle_evtrequest(evt),

        }

    def handle(self, evt: Event) -> Command | None:
        """
        Process an application event and convert it into CLI output.

        The handler inspects the event type and performs the appropriate
        action for the CLI environment. Typical actions include logging
        informational messages, displaying progress updates, reporting
        errors, or printing command results.

        Args:
            evt: An application event emitted by `App.run()`.

        Returns:
            None
        FIX: update docstring
        """
        event = self._events.get(type(evt))
        if event is None:
            logger.critical(f"Event not found in _events: {type(evt).__name__}")
        return event(evt)
        # if isinstance(evt, EvtLog):
        #     logger.info("%s", evt.message)
        #     return None
        # elif isinstance(evt, EvtProgress):
        #     # Build progressbar
        #     return None
        # elif isinstance(evt, EvtError):
        #     logger.error("%s - Fatal=%s", evt.message, evt.fatal)
        #     return None
        # elif isinstance(evt, EvtResult):
        #     logger.info("Handling EvtResult ..")
        #     print(f"{evt.command_name} - {evt.payload}")
        #     return None
        # elif isinstance(evt, EvtRequest):
        #     logger.info("Requesting from user")
        #     # call request function, get returned frontendinputcommand, 
        #     # send frontendinputcommand to build_command(), return the built command
        #     return None
        # else:
        #     logger.warning("Unhandled event type: %s", type(evt).__name__)
        #     return None

    def _handle_evtlog(self, evt) -> None:
        return None
    def _handle_evtprogress(self, evt) -> None:
        return None
    def _handle_evterror(self, evt) -> None:
        return None
    def _handle_evtresult(self, evt) -> None:
        logger.info(f"{evt.command_name}: {evt.payload}")
        return None
    def _handle_evtrequest(self, evt) -> None:
        return None
