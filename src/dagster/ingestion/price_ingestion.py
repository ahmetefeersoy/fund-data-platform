from .tefas_parser import TefasCrawler
from dagster import asset

@asset
def get_tefas_prices():
    crawler = TefasCrawler()

    data = crawler.fetch_historical_data(start_date="2020-01-01")
    return data