import pandas as pd
import numpy as np


def calculate_returns(prices: pd.Series, days: int) -> float:
    """Calculate simple returns over a given number of days."""
    if len(prices) < days:
        return None
    return (prices.iloc[-1] - prices.iloc[-days]) / prices.iloc[-days]


def calculate_fund_performance(fund_prices: pd.Series, category_prices: dict) -> dict:
    """Calculate performance metrics for a fund compared to its category peers."""
    if fund_prices.empty or len(fund_prices) < 30:
        return None
    
    returns_30d = calculate_returns(fund_prices, 30)
    returns_90d = calculate_returns(fund_prices, 90)
    returns_180d = calculate_returns(fund_prices, 180)
    
    if returns_90d is None:
        return None
    
    category_returns = [calculate_returns(p, 90) for p in category_prices.values() if calculate_returns(p, 90) is not None]
    
    if len(category_returns) < 2:
        return None
    
    category_avg = np.mean(category_returns)
    threshold = np.percentile(category_returns, 20)
    
    is_underperforming = returns_90d <= threshold
    rank = sum(1 for r in category_returns if r >= returns_90d)
    
    if is_underperforming:
        confidence = min(1.0, abs(returns_90d - threshold) / (abs(threshold) + 0.001) * 2)
    else:
        confidence = 0.0
    
    z_score = (returns_90d - category_avg) / (np.std(category_returns) + 0.001)
    performance_score = max(0, min(1, (z_score + 3) / 6))
    
    return {
        'performance_score': performance_score,
        'returns_30d': returns_30d,
        'returns_90d': returns_90d,
        'returns_180d': returns_180d,
        'category_avg_return': category_avg,
        'category_rank': rank,
        'total_peers': len(category_returns),
        'is_underperforming': is_underperforming,
        'confidence_score': confidence
    }
