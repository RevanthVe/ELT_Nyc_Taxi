import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from airflow.dags.ingest_data_local_script import data_ingest

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE=os.getenv('PG_DATABASE')

local_workflow = DAG(
    "Local_Data_Ingestion",
    schedule_interval="0 7 2 * *",
    start_date=datetime(2023, 1, 1)
)

URL_PREFIX = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{execution_date.strftime(\'%Y-%m\')}}.parquet'
INPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/input_{{execution_date.strftime(\'%Y-%m\')}}.parquet'
TABLE_NAME_TEMPLATE= 'yellow_tripdata_{{execution_date.strftime(\'%Y_%m\')}}'
with local_workflow:
    wget_task = BashOperator(
        task_id='wget',
        bash_command = f'curl -sSL {URL_TEMPLATE} > {INPUT_FILE_TEMPLATE}'
    )

    ingest_task = PythonOperator(
        task_id='ingest',
        python_callable=data_ingest,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=TABLE_NAME_TEMPLATE,
            file=INPUT_FILE_TEMPLATE
        ),
    )

    wget_task >> ingest_task