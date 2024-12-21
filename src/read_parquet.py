import os
import fireducks.pandas as pd


PARQUET_FILE = os.path.join(os.path.dirname(__file__), "DATA", "output_data.parquet")


def read_parquet(path, return_first=False):
    """
    I am happy function that hide my creator mistakes. I believe he wanted
    good :D

    Args:
        path (str): path to path that need to be load
        return_first (bool, optional): If `True`, function will return only
            first row of data :)


    Returns:
        type (pandas.DataFrame): no shit! I am returning your data saved in
            parquet format, NO PROBLEMO MINE FRIENDO!!! You may ask where i
            can provide path to my data?  OH you silly, you have me,
            you don't need any path.
    """
    if return_first:
        df = pd.read_parquet(path, engine="pyarrow").head(100).T
        first_row_list = df.iloc[0].tolist()
        return first_row_list
    
    df = pd.read_parquet(path, engine="pyarrow")
    return df


def save_data_batch(df, number):
    df_first_100 = df.head(number)
    df_first_100.to_parquet(f'first_{number}_rows.parquet', index=False)
    return os.path.abspath(f'first_{number}_rows.parquet')

if __name__ == "__main__":
    first_row = read_parquet(PARQUET_FILE, True)
    print(first_row)

    # df.iloc[0].to_json("first_row.json", orient="split")
