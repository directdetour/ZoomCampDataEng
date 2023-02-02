from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from prefect_gcp.bigquery import DatabaseBlock


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"gcspull/")
    return Path(f"gcspull/{gcs_path}")

@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    
    # Homework specifies to skip the transform
    #     
    # print(f"pre: Missing passengers count: {df['passenger_count'].isna().sum()}")
    # df['passenger_count'].fillna(0, inplace=True)
    # print(f"post: Missing passengers count: {df['passenger_count'].isna().sum()}")
    return df

@task()
def write_bq(df: pd.DataFrame, table_name: str) -> None:
    """Write DataFrame to Big Query"""    
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table=table_name,
        project_id="dtc-de-course-375819",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
        )

@flow(log_prints=True)
def etl_gcs_to_bq(year: int, month: int, color: str) -> int:
    """Main ETL Flow - data to Big Query DW"""  

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    print(f"rows processed: {len(df)}")
    
    table_name = f"dezoommodule2.{color}-rides"     

    write_bq(df, table_name)
    return len(df)

@flow(log_prints=True)
def gcs_to_pq_parent(
    months: list[int] = [1,2], 
    year: int = 2021, 
    color: str = "yellow"
    ):
    rows_processed = 0 
    for month in months:
        file_row_count = etl_gcs_to_bq(year, month, color)
        rows_processed += file_row_count    
    print(f"Total rows processed: {rows_processed}")
    

if __name__ == "__main__":
    color="yellow"
    months=[2,3]
    year=2019
    gcs_to_pq_parent(months, year, color)