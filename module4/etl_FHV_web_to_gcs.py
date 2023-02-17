from pathlib import Path
import pandas as pd
import numpy as np
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DF"""
    # if randint(0,1) > 0:
    #    raise Exception
    print(dataset_url)
    df = pd.read_csv(dataset_url, low_memory=False, encoding='latin1')
    return df

@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write Dataframe to a local file"""
    path =f"/workspaces/ZoomCampDataEng/module4/tmp/{dataset_file}.csv.gz"
    
    
    df.to_csv(path, compression="gzip", encoding='utf-8')

    return path

@task()
def write_gcs(path: Path) -> None:
    """Upload file to GCS"""    
    gcp_cloud_storage_bucket_block = GcsBucket.load("dtc-datalake-csv-myoung")
    gcp_cloud_storage_bucket_block.upload_from_path(path) 


@flow(log_prints=True)
def etl_fhv_to_gcs(year: int, month: int) -> None:
    dataset_file =f"fhv_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"
                     #https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2020-01.csv.gz
    df = fetch(dataset_url)
    path = write_local(df, dataset_file)
    write_gcs(path)    


@flow()
def etl_parent_flow(
    months: list[int] = [], years: list[int] = []
):
    for year in years:
        for month in months:
            etl_fhv_to_gcs(year, month)


if __name__ == "__main__":
    months=np.arange(2,3).tolist()
    years=[2020]
    etl_parent_flow(months, years)