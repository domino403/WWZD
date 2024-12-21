from read_parquet import read_parquet, PARQUET_FILE, save_data_batch
import fireducks.pandas as pd



if __name__ == "__main__":
    # test_data_path = save_data_batch(read_parquet(PARQUET_FILE), 100)
    TEST_FILE_PATH = r"C:\Users\dgil\Documents\git-repo\WWZD" \
                     r"\data_transformation\first_100_rows.parquet"
    df = read_parquet(TEST_FILE_PATH)
