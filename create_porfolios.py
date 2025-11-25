import requests
import random
import pandas as pd
from datetime import datetime, timedelta

API_BASE = "http://localhost:8000"

df = pd.read_csv("data/fund_labels_202511180330.csv")
fund_codes = df['code'].tolist()

def create_portfolio(name, positions):
    response = requests.post(
        f"{API_BASE}/portfolios/",
        json={
            "name": name,
            "description": f"Auto-generated portfolio {name}",
            "positions": positions
        }
    )
    return response.json()

def generate_random_portfolio(portfolio_num):
    selected_funds = random.sample(fund_codes, 3)
    
    weights = [random.uniform(5, 40) for _ in range(3)]
    total = sum(weights)
    weights = [round(w / total * 100, 2) for w in weights]
    weights[-1] = round(100 - sum(weights[:-1]), 2)
    
    positions = [
        { 
            "fund_code": fund,
            "weight": weight,
            "purchase_date": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "purchase_price": round(random.uniform(0.5, 5.0), 4)
        }
        for fund, weight in zip(selected_funds, weights)
    ]
    
    return create_portfolio(f"Portfolio_{portfolio_num+76}", positions)

if __name__ == "__main__":
    print("Creating 20+ portfolios...")
    
    for i in range(1, 21):
        try:
            portfolio = generate_random_portfolio(i)
            print(f"Created: {portfolio['name']} with {len(portfolio['positions'])} positions")
        except Exception as e:
            print(f"Error creating portfolio {i}: {e}")
    
    print("\nDone! Created 55 portfolios.")
