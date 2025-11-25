from dagster import job
from .risk_analytics_ops import (
    fetch_portfolio_positions,
    fetch_fund_prices,
    calculate_portfolio_risks,
    save_portfolio_risks
)
from .performance_analytics_ops import (
    fetch_all_funds_with_categories,
    fetch_historical_prices_for_performance,
    calculate_fund_performance_op,
    save_fund_performance
)


@job
def portfolio_risk_job():
    """
    Daily job to calculate portfolio risk.
    """
    portfolios = fetch_portfolio_positions()
    prices = fetch_fund_prices(portfolios)
    risks = calculate_portfolio_risks(portfolios, prices)
    save_portfolio_risks(risks)


@job
def fund_performance_job():
    """
    Daily job to evaluate funds performance.
    """
    funds = fetch_all_funds_with_categories()
    prices = fetch_historical_prices_for_performance(funds)
    performance = calculate_fund_performance_op(funds, prices)
    save_fund_performance(performance)
