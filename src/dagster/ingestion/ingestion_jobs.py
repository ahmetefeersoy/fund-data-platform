from dagster import job
from .ingestion_ops import get_tefas_prices, save_tefas_prices;

@job
def ingestion_job():
    save_tefas_prices(get_tefas_prices())
    