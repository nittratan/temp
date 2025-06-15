import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger("nextgen")
    logger.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler with rotation
    log_file = os.getenv("LOG_FILE", "nextgen.log")
    fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

logger = setup_logger()
