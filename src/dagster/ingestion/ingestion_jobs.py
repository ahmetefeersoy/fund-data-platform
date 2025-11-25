from dagster import job
from .ingestion_ops import get_tefas_prices, save_tefas_prices,clean_oldest_tefas_prices, get_daily_latest_tefas_prices

@job
def fetch_and_save_tefas_prices():
    data = get_tefas_prices()
    save_tefas_prices(data)

@job
def daily_tefas_price_update():
    daily_data = get_daily_latest_tefas_prices()
    save_tefas_prices(daily_data)
    clean_oldest_tefas_prices()