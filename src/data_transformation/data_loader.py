import polars as pl


class data_loader:
    def __init__(self, data_path: str):
        # data_df = read_parquet(data_path)
        print("Data loader initialized")
        pass

    def load_parquet(self, data_path: str):
        """
        Reads a Parquet file using the Polars library and measures the time taken.
        """
        print("Reading data using polars:")
        table = pl.read_parquet(data_path)
        return table
