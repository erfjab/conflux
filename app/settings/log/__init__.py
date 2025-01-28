from ._logger import LoggerSetup

logger = LoggerSetup(name="conflux").get_logger()

__all__ = ["logger"]