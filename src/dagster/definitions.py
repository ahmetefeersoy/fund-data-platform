from dagster import Definitions
from src.dagster.ingestion.ingestion_jobs import ingestion_job

defs = Definitions(
   
    jobs=[ingestion_job]
)
