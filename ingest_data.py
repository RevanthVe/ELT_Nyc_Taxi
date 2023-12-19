import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    file = 'output.parquet'

    os.system(f"wget {url} --output-document={file}")

    parquet_data = pd.read_parquet(file)

    parquet_data.to_csv(table_name, index=False)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(table_name,iterator = True, chunksize = 200000,low_memory= False)

    df = next(df_iter)

    df.head(n=0).to_sql(name=table_name,con=engine,if_exists="replace")

    try:
        while True:
            start_time = time()
            chunk = next(df_iter)
            chunk.to_sql(name=table_name,con=engine,if_exists="append")
            end_time = time()
            time_taken = end_time - start_time
            print(f"Inserted another chunk, it took {time_taken:.3f} seconds")
    except StopIteration:
        print("Reached end of the iterator.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest source data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table to write the results')
    parser.add_argument('--url', help='url of the souce file')

    args = parser.parse_args()

    main(args)



