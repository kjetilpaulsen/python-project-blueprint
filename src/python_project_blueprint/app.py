import logging

from python_project_blueprint.commands.commands import DisplayVersion
from python_project_blueprint.runtime.runtime import AppPaths, CFGDataBase, CFGDev, MetaInfo


logger = logging.getLogger(__name__)

class App:
    """
    The main app! This object will run most of the program
    """
    def __init__(self, meta: MetaInfo, dev: CFGDev, db: CFGDataBase, paths: AppPaths) -> None:
        logger.debug("Start ..")
        self.meta = meta
        self.dev = dev
        self.db = db
        self.paths = paths
        self.dev = dev
        self.db = db
        self.paths = paths

        # Start services..

        logger.debug("End ..")
        return None

    def _handle_command(self, cmd):
        if isinstance(cmd, DisplayVersion):
            logger.info(f"Version: {self.meta.app_version}")
        yield "Yielding event"

    def _handle_event(self, evt):
        logger.info(f"{evt}")

    def run(self, cmds: tuple) -> None:
        """
        Running headless version, takes in the argv list from terminal
        """
        logger.debug("Start ..")
        self._run_loop(cmds)
        logger.debug("End ..")

    def _run_loop(self, cmds) -> None:
        for cmd in cmds:
            for evt in self._handle_command(cmd):
                self._handle_event(evt)

        return None

