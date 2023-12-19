import os
import pandas as pd
from sqlalchemy import create_engine

os.system("wget https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv")

df_zones = pd.read_csv("taxi+_zone_lookup.csv")

print(df_zones.head())

engine = create_engine(f'postgresql://root:root@localhost:5432/ny_taxi')

df_zones.to_sql(name="taxi_zones",con=engine,if_exists="replace")