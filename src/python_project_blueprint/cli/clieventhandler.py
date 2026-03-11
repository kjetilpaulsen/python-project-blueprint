from __future__ import annotations

import logging
import sys

from python_project_blueprint.events.events import Event, EvtError, EvtLog, EvtProgress, EvtResult

logger = logging.getLogger(__name__)

class CliEventHandler:
    def __init__(self) -> None:
        pass

    def handle(self, evt: Event) -> None:
        if isinstance(evt, EvtLog):
            logger.info(f"{evt.message}")
        elif isinstance(evt, EvtProgress):
            # Build progressbar
            pass
        elif isinstance(evt, EvtError):
            logger.error(f"{evt.message}")
            if evt.fatal:
                sys.exit(evt.exit_code)
        elif isinstance(evt, EvtResult):
            print(f"{evt.command_name} - {evt.payload}")
        else:
            logger.warning(f"Unhandled event type: {type(evt).__name__}")
