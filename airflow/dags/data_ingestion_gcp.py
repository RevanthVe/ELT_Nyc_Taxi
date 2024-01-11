import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

from ingest_data_gcp_script import upload_to_gcs

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

URL_PREFIX = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{execution_date.strftime(\'%Y-%m\')}}.parquet'
INPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/input_{{execution_date.strftime(\'%Y-%m\')}}.parquet'
TABLE_NAME_TEMPLATE= 'yellow_tripdata_{{execution_date.strftime(\'%Y_%m\')}}.parquet'
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'nyc_taxi_raw1')


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023,1,1),
    "end_date":datetime(2023, 9, 30),
    "depends_on_past": False,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="0 7 2 * *",
    default_args=default_args,
    catchup=True,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:
    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sSL {URL_TEMPLATE} > {INPUT_FILE_TEMPLATE}"
    )

    # TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs=dict(
            bucket=BUCKET,
            object_name= f"raw/{TABLE_NAME_TEMPLATE}",
            local_file=INPUT_FILE_TEMPLATE,
        ),
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{TABLE_NAME_TEMPLATE}"],
            },
        },
    )

    download_dataset_task >> local_to_gcs_task >> bigquery_external_table_task