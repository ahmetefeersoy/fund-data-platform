from dagster import job
from .ingestion_ops import get_tefas_prices, save_tefas_prices,clean_oldest_tefas_prices, get_daily_latest_tefas_prices

@job
def fetch_and_save_tefas_prices():
    """
    Fetch the TEFAS prices for all funds
    and save them into the database.
    """
    
    data = get_tefas_prices()
    save_tefas_prices(data)

@job
def daily_tefas_price_update():
    """
    Daily job that fetchs the latest TEFAS prices for all funds
    and updates the database accordingly.
    """
    daily_data = get_daily_latest_tefas_prices()
    save_tefas_prices(daily_data)
    clean_oldest_tefas_prices()