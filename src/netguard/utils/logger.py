import logging
import sys

def setup_logger(name: str = "netguard", level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a standardized logger instance.
    """
    logger_inst = logging.getLogger(name)
    if not logger_inst.handlers:
        logger_inst.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger_inst.addHandler(handler)
    return logger_inst

logger = setup_logger()
