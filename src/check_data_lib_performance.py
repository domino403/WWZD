import time
import os

PARQUET_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../data/output_data.parquet"
)

def check_time(funcion):
    def wrapper(*args, **kwargs):
        print("--------------------------------------")
        start_time = time.time()
        funcion(*args, **kwargs)
        end_time = time.time()
        print('Time taken: ', end_time - start_time)
    return wrapper


@check_time
def read_polar():
    print('Reading data using polars:')
    import polars as pl
    table = pl.read_parquet(PARQUET_FILE)
    del table
    

@check_time
def read_pyarrow():
    print('Reading data using pyarrow:')
    import pyarrow.parquet as pq
    table = pq.read_table(PARQUET_FILE)
    del table
    

@check_time
def read_pandas():
    print('Reading data using pandas:')
    import pandas as pd
    table = pd.read_parquet(PARQUET_FILE, engine="pyarrow")
    del table
    

if __name__ == "__main__":
    read_pandas()
    read_polar()
    read_pyarrow()
