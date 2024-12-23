import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    # initialize logger
    logger = logging.getLogger("WWZD")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger

    # create console handler and set level to debug
    console_channel = logging.StreamHandler()
    console_channel.setLevel(logging.WARNING)

    file_handler = RotatingFileHandler(
        "WWZD.log", mode="a", maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s"
    )
    console_channel.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(console_channel)
    logger.addHandler(file_handler)

    return logger
