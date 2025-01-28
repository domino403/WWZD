"""
Transform a JSON DATA file into a Parquet file.


Please, do not ask 'why?'

I don't want talk about it.
"""

import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


json_file = os.path.join(os.path.dirname(__file__), "output.json")
parquet_file = os.path.join(os.path.dirname(__file__), "output_data.parquet")

chunk_size = 10000

writer = None

try:
    for chunk in pd.read_json(json_file, lines=True, chunksize=chunk_size):
        table = pa.Table.from_pandas(chunk)

        if writer is None:
            writer = pq.ParquetWriter(parquet_file, table.schema, compression="gzip")
        writer.write_table(table)

finally:
    if writer:
        writer.close()

print(f"saved in: {parquet_file}")
