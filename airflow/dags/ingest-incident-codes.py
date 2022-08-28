"""
  San Francisco Police Department Incident Code Ingestion
  Written by Tony Fong
"""

import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from pendulum import datetime
import pyarrow.csv as pv
import pyarrow.parquet as pq
import pandas as pd

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET_ID = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "sf_crime_data_all")
APP_TOKEN = os.environ.get("SODA_APP_TOKEN")

dataset_soda_api_url = f"https://data.sfgov.org/resource/ci9u-8awy.csv?$$app_token={APP_TOKEN}"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


def download_incident_codes(outputfile):
    df = pd.read_csv(dataset_soda_api_url)
    df.to_csv(outputfile, index=False)

def format_to_parquet(src_file):
    if not src_file.endswith(".csv"):
        logging.error("Can only process source files in CSV format.")
        return
    
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace(".csv", ".parquet"))


"""
	NOTE:  takes 20 minutes, at an upload speed of 800kbps.  Faster if your Internet has better upload speed
	Reference:  https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
	:param bucket: GCS bucket name
	:param object_name: target path & filename
	:param local_file: source path & filename
	:return:
"""
def upload_to_gcs(bucket, object_name, local_file):
	
	client = storage.Client()
	bucket = client.bucket(bucket)

	blob = bucket.blob(object_name)
	blob.upload_from_filename(local_file)


"""
    Ingest incident codes to Google Cloud Storage/BigQuery
"""
def ingest_incident_codes(
    dag,
    local_csv_path,
    local_parquet_path,
    gcs_parquet_path
    ):
    with dag:

        download_dataset_task = PythonOperator(
            task_id = "download_incident_codes",
            python_callable=download_incident_codes,
            op_kwargs=dict(
                outputfile = f"{local_csv_path}"
            )
        )

        format_to_parquet_task = PythonOperator(
            task_id = "format_to_parquet",
            python_callable = format_to_parquet,
            op_kwargs = dict(
                src_file = f"{local_csv_path}"
            )
        )

        local_to_gcs_task = PythonOperator(
            task_id = "local_to_gcs",
            python_callable = upload_to_gcs,
            op_kwargs = dict(
                bucket = BUCKET_ID,
                object_name = f"{gcs_parquet_path}",
                local_file = f"{local_parquet_path}"
            )
        )

        bigquery_external_table_task = BigQueryCreateExternalTableOperator(
            task_id = "bigquery_external_table_task",
            table_resource = {
                "tableReference": {
                    "projectId": PROJECT_ID,
                    "datasetId": BIGQUERY_DATASET,
                    "tableId": "external_incident_codes"
                },
                "externalDataConfiguration": {
                    "autodetect": "True",
                    "sourceFormat": "PARQUET",
                    "sourceUris": [f"gs://{BUCKET_ID}/{gcs_parquet_path}"]
                }
            }
        )

        remove_temporary_files_task = BashOperator(
            task_id = "remove_local_files",
            bash_command = f"rm {local_csv_path} {local_parquet_path}"
        )

        download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task >> remove_temporary_files_task



default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1
}


sf_incident_codes_dag = DAG(
    dag_id="ingest_sf_incident_codes_gcs",
    schedule_interval="@once",
    default_args=default_args,
    catchup=False,
    max_active_runs=1
)


sf_incident_codes_csv_file = "sfpd_incident_codes.csv"
sf_incident_codes_parquet_file = sf_incident_codes_csv_file.replace(".csv", ".parquet")
sf_incident_codes_csv_path = f"{path_to_local_home}/{sf_incident_codes_csv_file}"
sf_incident_codes_parquet_path = f"{path_to_local_home}/{sf_incident_codes_parquet_file}"
sf_incident_codes_gcs_parquet_path = f"raw/sf_crime_data/incident_codes/{sf_incident_codes_parquet_file}"

ingest_incident_codes(
    dag=sf_incident_codes_dag,
    local_csv_path=sf_incident_codes_csv_path,
    local_parquet_path=sf_incident_codes_parquet_path,
    gcs_parquet_path=sf_incident_codes_gcs_parquet_path
)
