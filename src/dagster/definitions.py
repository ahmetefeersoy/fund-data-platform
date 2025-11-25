from dagster import Definitions, ScheduleDefinition
from src.dagster.ingestion.ingestion_jobs import (
    fetch_and_save_tefas_prices,
    daily_tefas_price_update,
)


daily_tefas_price_update_schedule = ScheduleDefinition(
    name="daily_tefas_price_update_schedule",
    cron_schedule="0 2 * * *",
    job=daily_tefas_price_update,
)


defs = Definitions(
    jobs=[fetch_and_save_tefas_prices, daily_tefas_price_update],
    schedules=[daily_tefas_price_update_schedule],
)