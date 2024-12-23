import os
import time

import polars as pl

from logging_config import setup_logger


LOGGER = setup_logger()


class data_menager:
    """
    Class to manage data loading and preparation.

    Attributes:
        data_path (str): Path to the data file.
        DataFrame (pl.DataFrame): Loaded and prepared data.
    """

    def __init__(self, data_path: str):
        """
        Initialize the DataManager with the path to the data file.

        Args:
            data_path (str): Path to the data file.
        """
        LOGGER.info(f"Data menager initialized, input path: '{data_path}'")

        self.data_path = os.path.abspath(data_path)
        self.DataFrame = None

    def load_parquet(self):
        """
        Load data from a parquet file into a Polars DataFrame.

        Raises:
            Exception: If there is an error while loading the parquet file.
        """
        LOGGER.info(f"Checking if '{self.data_path}' exists")
        if not os.path.exists(self.data_path):
            LOGGER.error(f"Path '{self.data_path}' does not exist.")
            raise FileNotFoundError(f"Path '{self.data_path}' does not exist.")

        try:
            LOGGER.info(f"Starting to load parquet file from '{self.data_path}'")
            start_time = time.time()
            self.DataFrame = pl.read_parquet(self.data_path)
            LOGGER.info(
                f"Parquet file loaded successfully. Time taken:  {time.time() - start_time}"
            )

        except Exception as e:
            LOGGER.error(f"Error while loading parquet file: {e}", exc_info=True)

    def prepare_data(self):
        """
        Prepare the loaded data by transposing, renaming columns, and extracting image parameters.

        Raises:
            ValueError: If no data is loaded yet.
        """
        if self.DataFrame is None:
            LOGGER.error("No data loaded yet.")
            raise ValueError("No data loaded yet.")

        LOGGER.info("## Preparing data - DataFrame ##")
        start_time = time.time()
        self.DataFrame = self.DataFrame.transpose(
            include_header=True, column_names=["image_params_list"]
        )
        self.DataFrame = self.DataFrame.rename({"column": "image_ID"})
        LOGGER.info(
            f"Transposed to DataFrame{self.DataFrame.shape} with column names: {self.DataFrame.columns}"
        )

        self.DataFrame = self.DataFrame.lazy().with_columns(
            pl.col("image_params_list").list.to_array(1000).alias("image_params_array"),
        )
        self.DataFrame = self.DataFrame.lazy().drop("image_params_list")
        self.DataFrame = (
            self.DataFrame.lazy()
            .with_columns(
                pl.col("image_params_array").arr.to_struct(
                    fields=[f"param_{x}" for x in range(1000)]
                ),
            )
            .unnest("image_params_array")
        )
        LOGGER.info("Etracted image_params_list to separated columns.")

        self.DataFrame = self.DataFrame.collect()
        LOGGER.info(
            f"Data preparation completed. Final shape: {self.DataFrame.shape}, Time taken:  {time.time() - start_time}"
        )
