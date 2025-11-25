from .tefas_parser import TefasCrawler
from dagster import op, OpExecutionContext, Field , RetryPolicy
from datetime import date, timedelta


@op(config_schema={"window_days": Field(int, default_value=270)}, retry_policy=RetryPolicy(max_retries=3, delay=15)) 
def get_tefas_prices(context: OpExecutionContext):
    crawler = TefasCrawler()

    window = context.op_config["window_days"]
    end = date.today()
    start = end - timedelta(days=window)

    data = crawler.fetch_historical_data(start_date=start, end_date=end)
    return data


@op(retry_policy=RetryPolicy(max_retries=3, delay=15))
def get_daily_latest_tefas_prices():
    crawler = TefasCrawler()
    end = date.today() - timedelta(days=1)
    start = end 
    data = crawler.fetch_historical_data(start_date=start, end_date=end)
    return data

@op(retry_policy=RetryPolicy(max_retries=3, delay=15))
def clean_oldest_tefas_prices():
    crawler = TefasCrawler()
    crawler.clean_oldest_data()
    

@op(retry_policy=RetryPolicy(max_retries=3, delay=15))
def save_tefas_prices(data):
    crawler = TefasCrawler()
    crawler.save_to_db(data)