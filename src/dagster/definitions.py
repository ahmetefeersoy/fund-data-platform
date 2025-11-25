from dagster import Definitions, ScheduleDefinition
from src.dagster.ingestion.ingestion_jobs import (
    fetch_and_save_tefas_prices,
    daily_tefas_price_update,
)
from src.dagster.analytics.analytics_jobs import (
    portfolio_risk_job,
    fund_performance_job,
)


# 2 AM daily update of TEFAS prices
daily_tefas_price_update_schedule = ScheduleDefinition(
    name="daily_tefas_price_update_schedule",
    cron_schedule="0 2 * * *",
    job=daily_tefas_price_update,
)

# 3 AM daily portfolio risk calculation
portfolio_risk_schedule = ScheduleDefinition(
    name="portfolio_risk_schedule",
    cron_schedule="0 3 * * *", 
    job=portfolio_risk_job,
)
# 3 AM daily fund performance evaluation
fund_performance_schedule = ScheduleDefinition(
    name="fund_performance_schedule",
    cron_schedule="0 3 * * *",  
    job=fund_performance_job,
)


defs = Definitions(
    jobs=[
        fetch_and_save_tefas_prices, 
        daily_tefas_price_update,
        portfolio_risk_job,
        fund_performance_job,
    ],
    schedules=[
        daily_tefas_price_update_schedule,
        portfolio_risk_schedule,
        fund_performance_schedule,
    ],
)