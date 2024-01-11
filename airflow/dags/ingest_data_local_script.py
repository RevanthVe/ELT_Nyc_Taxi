
import pandas as pd
from sqlalchemy import create_engine
from time import time

def data_ingest(user,password,host,port,db,table_name,file):
    print(table_name,file)

    parquet_data = pd.read_parquet(file)
    parquet_data.to_csv(table_name, index=False)
    print("converted data type from parquet to csv")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    print("connection established successfully with database,insering data..")

    start_time = time()
    df_iter = pd.read_csv(table_name,iterator = True, chunksize = 200000,low_memory= False)
    df = next(df_iter)
    df.head(n=0).to_sql(name=table_name,con=engine,if_exists="replace")
    df.to_sql(name=table_name,con=engine,if_exists="append")
    end_time=time()
    print(f"Inserted another chunk, it took {(end_time-start_time):.3f} seconds")

    try:
        while True:
            start_time = time()
            chunk = next(df_iter)
            chunk.to_sql(name=table_name,con=engine,if_exists="append")
            end_time = time()
            print(f"Inserted another chunk, it took {(end_time-start_time):.3f} seconds")
    except StopIteration:
        print("Reached end of the iterator.")