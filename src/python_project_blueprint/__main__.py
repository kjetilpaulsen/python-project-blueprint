# FIX: Change imports from "python_project_blueprint" to packagename
import logging
import sys

from python_project_blueprint.entrypoints import cli_main, api_main
from python_project_blueprint.identity import IDENTITY
from python_project_blueprint.utils.logging.loggingsetup import setup_basic_logging



def main() -> int:
    """
    Starts basic logging and decides between entrypoints.
    """
    setup_basic_logging()
    logger = logging.getLogger(IDENTITY.logger_name)
    logger.info("Basic logging started")

    argv = sys.argv[1:]
    if not argv:
        logger.warning(f"Usage: {IDENTITY.package_name} [cli|api] ...")
        return 2
    
    mode, *rest = argv

    if mode == "cli":
        return cli_main(rest)

    if mode == "api":
        return api_main(rest)

    logger.warning(f"Unknown entrypoint: {mode}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
