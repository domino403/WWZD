import time
import os

PARQUET_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../data/output_data.parquet"
)


def check_time(funcion):
    """
    Decorator function to measure the execution time of a function.

    Args:
        funcion (function): The function to be wrapped.

    Returns:
        function: The wrapped function with execution time measurement.
    """

    def wrapper(*args, **kwargs):
        print("--------------------------------------")
        start_time = time.time()
        funcion(*args, **kwargs)
        end_time = time.time()
        print("Time taken: ", end_time - start_time)

    return wrapper


@check_time
def read_polar():
    """
    Reads a Parquet file using the Polars library and measures the time taken.
    """
    print("Reading data using polars:")
    import polars as pl

    table = pl.read_parquet(PARQUET_FILE)
    del table


@check_time
def read_pyarrow():
    """
    Reads a Parquet file using the PyArrow library and measures the time taken.
    """
    print("Reading data using pyarrow:")
    import pyarrow.parquet as pq

    table = pq.read_table(PARQUET_FILE)
    del table


@check_time
def read_pandas():
    """
    Reads a Parquet file using the Pandas library and measures the time taken.
    """
    print("Reading data using pandas:")
    import pandas as pd

    table = pd.read_parquet(PARQUET_FILE, engine="pyarrow")
    del table


if __name__ == "__main__":
    """
    Main function to execute the performance checks for different libraries.
    """
    read_pandas()
    read_polar()
    read_pyarrow()
