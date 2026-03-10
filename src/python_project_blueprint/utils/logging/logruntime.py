
import logging
from python_project_blueprint.runtime.runtime import Runtime

logger = logging.getLogger(__name__)

def log_runtime(rt: Runtime) -> None:
    """
    Logs the settings of the current run. Except secrets
    """
    logger.info("Logging runtime settings, except DB/secrets")
    logger.info(f"{rt.meta.app_name=}")
    logger.info(f"{rt.meta.app_version=}")
    logger.info(f"{rt.meta.app_description=}")
    logger.info(f"{rt.paths.data_dir=}")
    logger.info(f"{rt.paths.state_dir=}")
    logger.info(f"{rt.paths.cache_dir=}")
    logger.info(f"{rt.paths.tmp_dir=}")
    logger.info(f"{rt.paths.config_dir=}")
    logger.info(f"{rt.paths.logs_dir=}")
    logger.info(f"{rt.dev.dev_mode=}")
    logger.info(f"{rt.dev.dry_run=}")
    logger.info(f"{rt.log.log_level=}")
    logger.info(f"{rt.log.console_level=}")
    logger.info(f"{rt.log.console_log=}")
    logger.info(f"{rt.log.stderr_log=}")

