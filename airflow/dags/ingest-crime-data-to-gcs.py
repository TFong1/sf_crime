"""
  SF Crime Data Ingestion
  Written by Tony Fong
"""

import imp
import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
#from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryUpsertTableOperator
from pendulum import datetime
import pyarrow.csv as pv
import pyarrow.parquet as pq
import pandas as pd

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET_ID = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "sf_crime_data_all")
APP_TOKEN = ""

dataset_soda_api_url = "https://data.sfgov.org/resource/wg3w-h783.json"
dataset_date_field = "incident_date"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")



# Save to .CSV file first
def download_crime_data(month, year, outputfile):
	url = f"{dataset_soda_api_url}?$$app_token={APP_TOKEN}&$where=date_extract_y({dataset_date_field})={year}%20and%20date_extract_m({dataset_date_field})={month}"
	df = pd.read_json(url)
	df.to_csv(outputfile, index=False)


# Read from CSV file and convert to parquet file
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
	Upload Parquetized Data to Google Cloud Storage
"""
def upload_parquetized_crime_data(
	dag,
	year,
	month,
	local_csv_path,
	local_parquet_path,
	gcs_parquet_path
	):
	with dag:

		download_dataset_task = PythonOperator(
			task_id="download_dataset_task",
			python_callable=download_crime_data,
			op_kwargs={
				"month": month,
				"year": year,
				"outputfile": local_csv_path
			}
		)

		format_to_parquet_task = PythonOperator(
			task_id="format_to_parquet_task",
			python_callable=format_to_parquet,
			op_kwargs={
				"src_file": local_csv_path
			}
		)

		local_to_gcs_task = PythonOperator(
			task_id="local_to_gcs_task",
			python_callable=upload_to_gcs,
			op_kwargs={
				"bucket": BUCKET_ID,
				"object_name": gcs_parquet_path,
				"local_file": local_parquet_path
			}
		)

		bigquery_external_table_task = BigQueryUpsertTableOperator(
			task_id="bigquery_external_table_task",
			dataset_id=BIGQUERY_DATASET,
			table_resource={
				"tableReference": {
					"projectId": PROJECT_ID,
					"datasetId": BIGQUERY_DATASET,
					"tableId": "external_table"
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
			bash_command=f"rm {local_csv_path} {local_parquet_path}"
		)

		#download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task >> remove_temporary_files_task
		download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> remove_temporary_files_task


default_args = {
	"owner": "airflow",
	"start_date": days_ago(1),
	"depends_on_past": False,
	"retries": 1
}

"""
# DAG declaration -- using a Contect Manager (an implicit way)
with DAG(
	dag_id="sf_crime_data_ingestion_gcs_dag",
	schedule_interval="@monthly",
	default_args=default_args,
	catchup=False,
	max_active_runs=1,
	tags=["sf-crime"]
) as dag:
"""

sf_crime_data_dag = DAG(
	dag_id="ingest_sf_crime_gcs",
	schedule_interval="@monthly",
	start_date=datetime(year=2020, month=1, day=1),
	default_args=default_args,
	catchup=False,
	max_active_runs=1
)

sf_crime_csv_file = "sf_crime_{{ macros.ds_format(ds, '%Y-%m-%d', '%Y-%m') }}.csv"
current_year = "{{ macros.ds_format(ds, '%Y-%m-%d', '%Y') }}"
current_month = "{{ macros.ds_format(ds, '%Y-%m-%d', '%m') }}"
sf_crime_parquet_file = sf_crime_csv_file.replace(".csv", ".parquet")
sf_crime_csv_path = f"{path_to_local_home}/{sf_crime_csv_file}"
sf_crime_parquet_path = f"{path_to_local_home}/{sf_crime_parquet_file}"
gcs_year_subfolder = "{{ macros.ds_format(ds, '%Y-%m-%d', '%Y') }}"
sf_crime_target_gcs_parquet_path = f"raw/sf_crime_data/{gcs_year_subfolder}/{sf_crime_parquet_file}"

upload_parquetized_crime_data(
	dag=sf_crime_data_dag,
	year=current_year,
	month=current_month,
	local_csv_path=sf_crime_csv_path,
	local_parquet_path=sf_crime_parquet_path,
	gcs_parquet_path=sf_crime_target_gcs_parquet_path
)
