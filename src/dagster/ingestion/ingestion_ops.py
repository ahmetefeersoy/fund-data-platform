from .tefas_parser import TefasCrawler
from dagster import op

@op
def get_tefas_prices():
    crawler = TefasCrawler()

    data = crawler.fetch_historical_data(start_date="2025-09-09", end_date="2025-09-09")
    return data

@op
def save_tefas_prices(data):
    crawler = TefasCrawler()
    crawler.save_to_db(data)