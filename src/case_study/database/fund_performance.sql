CREATE TABLE fund_performance (
    id SERIAL PRIMARY KEY,
    fund_code TEXT NOT NULL,
    calculation_date DATE NOT NULL, 
    performance_score NUMERIC NOT NULL,
    returns_30d NUMERIC,
    returns_90d NUMERIC,
    returns_180d NUMERIC,
    category_avg_return NUMERIC,
    category_rank INTEGER,
    total_peers INTEGER,
    is_underperforming BOOLEAN DEFAULT FALSE,
    confidence_score NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(fund_code, calculation_date)
);

CREATE INDEX idx_fund_performance_fund_date ON fund_performance(fund_code, calculation_date DESC);
CREATE INDEX idx_fund_performance_underperforming ON fund_performance(is_underperforming, calculation_date DESC);
CREATE INDEX idx_fund_performance_category ON fund_performance(calculation_date DESC, is_underperforming);
