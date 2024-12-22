import os

from logging_config import setup_logger
from src.data_transformation.data_menager import data_menager


LOGGER = setup_logger()


if __name__ == "__main__":
    LOGGER.info("Starting main.py!")
    LOGGER.info(f"Current working directory: '{os.getcwd()}'")
    data_loader = data_menager("data/output_data.parquet")
    data_loader.load_parquet()
    LOGGER.info("Data loading completed.")
    data_loader.prepare_data()
    LOGGER.info("Data preparation completed.")

    # print(data_loader.prepare_data().head(3))
    # LOGGER.info("Data loading completed.")
