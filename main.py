import logging
from logging.handlers import RotatingFileHandler

from src.data_transformation.data_loader import data_loader


def setup_logger():
    # initialize logger
    logger = logging.getLogger("WWZD_main")
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    console_channel = logging.StreamHandler()
    console_channel.setLevel(logging.WARNING)

    file_handler = RotatingFileHandler(
        "WWZD.log", mode="w", maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_channel.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add console_channel to logger
    logger.addHandler(console_channel)
    logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    logger = setup_logger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")
    data_loader = data_loader("data")
