import os

from logging_config import setup_logger
from src.data_transformation.data_menager import data_menager
from src.data_transformation.dim_reduction import pca_dim_reduction


LOGGER = setup_logger()


if __name__ == "__main__":
    LOGGER.info("Starting main.py!")
    LOGGER.info(f"Current working directory: '{os.getcwd()}'")
    data_loader = data_menager("data/output_data.parquet")
    data_loader.load_parquet()
    LOGGER.info("Data loading completed.")
    data_loader.prepare_data()
    LOGGER.info("Data preparation completed.")

    test = pca_dim_reduction(data_loader.DataFrame.head(50), 30)
    print(test)

    # TODO: Implement dimensionality reduction
    # - saving/loading system for dimensional reducted data. Run the dimensionality reduction only if the data is not already saved.

    # TODO: data visualisation
