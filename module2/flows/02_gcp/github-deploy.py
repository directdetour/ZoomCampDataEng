from prefect.deployments import Deployment
from etl_web_to_gcs import etl_parent_flow
from prefect.filesystems import GitHub 

storage = GitHub.load("github-module2")

deployment = Deployment.build_from_flow(
     flow=etl_parent_flow,
     name="github-example",
     storage=storage,
     entrypoint="module2/flows/02_gcp/etl_web_to_gcs.py:etl_parent_flow")

if __name__ == "__main__":
    deployment.apply()