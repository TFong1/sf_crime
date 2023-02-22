

import os
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(log_prints=True, retries=3)
def download_crime_data(year: int, month: int, outputfile: str) -> None:
    APP_TOKEN = os.environ.get("SODA_APP_TOKEN")
    return


@task(log_prints=True, retries=3)
def format_to_parquet(src_file: str) -> None:
    return


@task(log_prints=True, retries=3)
def upload_to_gcs(bucket, object_name, local_file) -> None:
    return



@flow(log_prints=True, retries=3)
def etl_web_to_gcs(year: int, month: int):
    """ This is the main ETL function  """
    dataset_soda_api_url = "https://data.sfgov.org/resource/wg3w-h783.json"
    dataset_date_field = "incident_date"
    dataset_file = ""
    dataset_url = f"{dataset_soda_api_url}?$$app_token={APP_TOKEN}&$where=date_extract_y({dataset_date_field})={year}%20and%20date_extract_m({dataset_date_field})={month}"
    df = pd.read_json(dataset_url)
    df

@flow(log_prints=True, retries=3)
def etl_crime_pipeline(
    year: int,
    months: list[int] = [1,2,3,4,5,6,7,8,9,10,11,12]
) -> None:
    return


if __name__ == "__main__":
    year = 2021