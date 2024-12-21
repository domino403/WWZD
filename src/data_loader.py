from read_parquet import read_parquet, save_data_batch, PARQUET_FILE


class data_loader:
    def __init__(self, data_path: str = PARQUET_FILE):
        data_df = read_parquet(data_path)
            
