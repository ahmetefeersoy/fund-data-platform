import pandas as pd
import numpy as np
from dagster import op , RetryPolicy
from datetime import datetime, timedelta
from sqlalchemy import text
from src.case_study.utils.db import engine
from src.case_study.analytics.risk import calculate_portfolio_risk


@op(retry_policy=RetryPolicy(max_retries=3, delay=15))
def fetch_portfolio_positions():
    query = """
        SELECT p.id AS portfolio_id, pos.fund_code, pos.weight
        FROM portfolios p
        JOIN positions pos ON p.id = pos.portfolio_id
    """
    with engine.connect() as conn:
        return pd.read_sql(query, conn)


@op(retry_policy=RetryPolicy(max_retries=3, delay=15))
def fetch_fund_prices(portfolios_data):
    fund_codes = portfolios_data["fund_code"].unique().tolist()
    if not fund_codes:
        return pd.DataFrame()

    end = datetime.now()
    start = end - timedelta(days=260)

    query = text("""
        SELECT code AS fund_code, date, price
        FROM fund_data
        WHERE code = ANY(:fund_codes)
          AND date BETWEEN :start AND :end
          AND price IS NOT NULL
        ORDER BY fund_code, date
    """)

    with engine.connect() as conn:
        return pd.read_sql(
            query, conn,
            params={"fund_codes": fund_codes, "start": start, "end": end}
        )


@op(retry_policy=RetryPolicy(max_retries=3, delay=15))
def calculate_portfolio_risks(portfolios_data, prices_data):
    if prices_data.empty:
        return pd.DataFrame()

    prices_data["date"] = pd.to_datetime(prices_data["date"])
    results = []

    for pid in portfolios_data["portfolio_id"].unique():
        pos = portfolios_data[portfolios_data["portfolio_id"] == pid]
        fund_codes = pos["fund_code"].tolist()

        p_prices = prices_data[prices_data["fund_code"].isin(fund_codes)]

        if p_prices.empty:
            continue

        price_matrix = p_prices.pivot(index="date", columns="fund_code", values="price")
        price_matrix = price_matrix.ffill() 

        if len(price_matrix) < 30:
            continue

        weights = pos.set_index("fund_code")["weight"] / 100
        weights = weights.reindex(price_matrix.columns).fillna(0).values

        portfolio_price_series = (
            price_matrix.values * weights
        ).sum(axis=1)

        risk = calculate_portfolio_risk(pd.Series(portfolio_price_series))

        results.append({
            "portfolio_id": pid,
            "calculation_date": datetime.now().date(),
            **risk
        })

    return pd.DataFrame(results)


@op(retry_policy=RetryPolicy(max_retries=3, delay=15))
def save_portfolio_risks(risks_data):
    if risks_data.empty:
        return

    query = text("""
        INSERT INTO portfolio_risks
            (portfolio_id, calculation_date, risk_score, risk_level, 
             volatility, sharpe_ratio, max_drawdown, var_95, days_analyzed)
        VALUES 
            (:portfolio_id, :calculation_date, :risk_score, :risk_level,
             :volatility, :sharpe_ratio, :max_drawdown, :var_95, :days_analyzed)
        ON CONFLICT (portfolio_id, calculation_date)
        DO UPDATE SET
            risk_score = EXCLUDED.risk_score,
            risk_level = EXCLUDED.risk_level,
            volatility = EXCLUDED.volatility,
            sharpe_ratio = EXCLUDED.sharpe_ratio,
            max_drawdown = EXCLUDED.max_drawdown,
            var_95 = EXCLUDED.var_95,
            days_analyzed = EXCLUDED.days_analyzed;
    """)

    with engine.begin() as conn:
        for _, row in risks_data.iterrows():
            conn.execute(query, row.to_dict())
