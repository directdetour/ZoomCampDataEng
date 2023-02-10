from pathlib import Path
import pandas as pd
import numpy as np
from prefect import flow, task
from prefect_azure import AzureBlobStorageCredentials
from prefect_azure.blob_storage import blob_storage_upload


from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DF"""
    # if randint(0,1) > 0:
    #    raise Exception
    print(dataset_url)
    df = pd.read_csv(dataset_url)
    return df

@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write Dataframe to a local file"""
    path =f"/workspaces/ZoomCampDataEng/module3/tmp/{dataset_file}.csv.gz"
    df.to_csv(path, compression="gzip")
    return path

@flow(log_prints=True)
def write_to_azure(path: Path, filename: str) -> None:
    """Upload file to Azure Storage"""    
    
    azure_credentials_block = AzureBlobStorageCredentials.load("az-blob-creds")
    with open(path, "rb") as f:
        blob = blob_storage_upload(
            data=f.read(),
            container="fhv",
            blob=filename,
            blob_storage_credentials=azure_credentials_block,
            overwrite=False,
        )
    


@flow(log_prints=True)
def etl_fhv_to_azure(year: int, month: int) -> None:
    dataset_file =f"fhv_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"
    
    #skipping fetch and write_local - these were already downloaded and saved locally.
    #df = fetch(dataset_url)
    #path = write_local(df, dataset_file)
    path = f"/workspaces/ZoomCampDataEng/module3/tmp/{dataset_file}.csv.gz"
    write_to_azure(path, f"{dataset_file}.csv.gz")

@flow()
def etl_parent_flow(
    months: list[int] = [], years: list[int] = []
):
    for year in years:
        for month in months:
            etl_fhv_to_azure(year, month)


if __name__ == "__main__":
    months=[2] #np.arange(1,13).tolist()
    years=[2019]
    etl_parent_flow(months, years)