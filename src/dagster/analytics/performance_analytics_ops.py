import pandas as pd
import numpy as np
from dagster import op
from datetime import datetime, timedelta
from sqlalchemy import text
from src.case_study.utils.db import engine
from src.case_study.analytics.performance import calculate_fund_performance


@op
def fetch_all_funds_with_categories():
    query = """
    SELECT 
        f.code as fund_code,
        f.category,
        f.main_category,
        f.title
    FROM funds f
    """
    
    with engine.connect() as conn:
        data = pd.read_sql(query, conn)
    
    return data


@op
def fetch_historical_prices_for_performance(funds_data):
    fund_codes = funds_data['fund_code'].unique().tolist()
    
    if not fund_codes:
        return pd.DataFrame()
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=270)
    
    query = text("""
    SELECT 
        code as fund_code,
        date,
        price
    FROM fund_data
    WHERE code = ANY(:fund_codes)
        AND date >= :start_date
        AND date <= :end_date
        AND price IS NOT NULL
    ORDER BY code, date
    """)
    
    with engine.connect() as conn:
        prices_data = pd.read_sql(query, conn, params={
            'fund_codes': fund_codes,
            'start_date': start_date,
            'end_date': end_date
        })
    
    return prices_data


@op
def calculate_fund_performance_op(funds_data, prices_data):
    if prices_data.empty:
        return pd.DataFrame()
    
    prices_data['date'] = pd.to_datetime(prices_data['date'])
    analysis_data = prices_data.merge(funds_data, on='fund_code', how='left')
    
    results = []
    
    for category in analysis_data['category'].dropna().unique():
        category_data = analysis_data[analysis_data['category'] == category]
        fund_codes = category_data['fund_code'].unique()
        
        category_prices = {}
        for fund_code in fund_codes:
            fund_data = category_data[category_data['fund_code'] == fund_code].sort_values('date')
            if len(fund_data) >= 30:
                category_prices[fund_code] = fund_data['price'].reset_index(drop=True)
        
        if len(category_prices) < 2:
            continue
        
        for fund_code, fund_prices in category_prices.items():
            perf = calculate_fund_performance(fund_prices, category_prices)
            
            if perf:
                results.append({
                    'fund_code': fund_code,
                    'calculation_date': datetime.now().date(),
                    **perf
                })
        
    
    return pd.DataFrame(results)


@op
def save_fund_performance(performance_data):
  
    if performance_data.empty:
        return
    
    
    with engine.begin() as conn:
        for _, row in performance_data.iterrows():
            query = text("""
            INSERT INTO fund_performance 
                (fund_code, calculation_date, performance_score, 
                 returns_30d, returns_90d, returns_180d,
                 category_avg_return, category_rank, total_peers,
                 is_underperforming, confidence_score)
            VALUES 
                (:fund_code, :calculation_date, :performance_score,
                 :returns_30d, :returns_90d, :returns_180d,
                 :category_avg_return, :category_rank, :total_peers,
                 :is_underperforming, :confidence_score)
            ON CONFLICT (fund_code, calculation_date) 
            DO UPDATE SET
                performance_score = EXCLUDED.performance_score,
                returns_30d = EXCLUDED.returns_30d,
                returns_90d = EXCLUDED.returns_90d,
                returns_180d = EXCLUDED.returns_180d,
                category_avg_return = EXCLUDED.category_avg_return,
                category_rank = EXCLUDED.category_rank,
                total_peers = EXCLUDED.total_peers,
                is_underperforming = EXCLUDED.is_underperforming,
                confidence_score = EXCLUDED.confidence_score,
                created_at = CURRENT_TIMESTAMP
            """)
            
            conn.execute(query, row.to_dict())
    
