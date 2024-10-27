import os
import pandas as pd


PARQUET_FILE = os.path.join(os.path.dirname(__file__), "DATA", "output_data.parquet")


def read_parquet(return_first=False):
    """
    I am happy function that hide my creator mistakes. I belive he wanted good :D

    Args:
        return_first (bool, optional): If `True`, function will return only first row of data :)

    Returns:
        type (pandas.DataFrame): no shit! I am returning your data saved in parquet format,
        NO PROBLEMO MINE FRIENDO!!! You may ask where i can provide path to my data? 
        OH you silly, you have me, you don't need any path.
    """
    if return_first:
        df = pd.read_parquet(PARQUET_FILE, engine="pyarrow").head(100).T
        first_row_list = df.iloc[0].tolist()
        return first_row_list
    
    df = pd.read_parquet(PARQUET_FILE, engine="pyarrow")
    return df


if __name__ == "__main__":
    first_row = read_parquet(True)
    print(first_row)

    # df.iloc[0].to_json("first_row.json", orient="split")
