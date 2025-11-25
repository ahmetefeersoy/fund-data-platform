import numpy as np
import pandas as pd
from math import sqrt
from typing import Dict


def calculate_volatility(returns: pd.Series) -> float:
    """Annualized volatility = std(returns) * sqrt(252)"""
    if returns.empty:
        return 0.0
    return returns.std() * np.sqrt(252)


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
    """
    Annualized Sharpe Ratio
    Sharpe = (mean(return) - risk_free_rate/252) / std(return)
    """
    if returns.empty or returns.std() == 0:
        return 0.0

    daily_rf = risk_free_rate / 252
    excess_return = returns.mean() - daily_rf
    
    return (excess_return / returns.std()) * np.sqrt(252)


def calculate_max_drawdown(prices: pd.Series) -> float:
    """Max drawdown = (peak - trough) / peak"""
    if prices.empty:
        return 0.0

    rolling_max = prices.cummax()
    drawdown = (prices - rolling_max) / rolling_max
    return drawdown.min()  


def calculate_var_95(returns: pd.Series) -> float:
    """Parametric VaR 95% (mean - 1.65 * std)"""
    if returns.empty:
        return 0.0

    return returns.mean() - 1.65 * returns.std()


def classify_risk_level(score: float) -> str:
    if score < 25:
        return "LOW"
    elif score < 60:
        return "MEDIUM"
    return "HIGH"


def calculate_portfolio_risk(prices: pd.Series) -> Dict:
    if prices.empty or len(prices) < 30:
        return {
            "risk_score": 0,
            "risk_level": "LOW",
            "volatility": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0,
            "var_95": 0,
            "days_analyzed": len(prices),
        }

    returns = prices.pct_change().dropna()

    volatility = calculate_volatility(returns)
    sharpe = calculate_sharpe_ratio(returns)
    max_dd = calculate_max_drawdown(prices)
    var95 = calculate_var_95(returns)

    vol_score = min(volatility * 250, 100)
    dd_score = min(abs(max_dd) * 200, 100)
    var_score = min(abs(var95) * 2500, 100)
    sharpe_score = max(0, min(100, 100 - (sharpe * 15)))
    
    score = (
        (vol_score * 0.35) +
        (dd_score * 0.35) +
        (var_score * 0.15) +
        (sharpe_score * 0.15)
    )

    score = float(np.clip(score, 0, 100))
    level = classify_risk_level(score)

    return {
        "risk_score": score,
        "risk_level": level,
        "volatility": float(volatility),
        "sharpe_ratio": float(sharpe),
        "max_drawdown": float(max_dd),
        "var_95": float(var95),
        "days_analyzed": len(prices),
    }
