
CREATE TABLE portfolio_risks (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL,
    calculation_date DATE NOT NULL,
    risk_score NUMERIC NOT NULL,
    risk_level TEXT NOT NULL CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH')),
    volatility NUMERIC,
    sharpe_ratio NUMERIC,
    max_drawdown NUMERIC,
    var_95 NUMERIC,
    days_analyzed INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(portfolio_id, calculation_date)
);

CREATE INDEX idx_portfolio_risks_portfolio_date ON portfolio_risks(portfolio_id, calculation_date DESC);
CREATE INDEX idx_portfolio_risks_level ON portfolio_risks(risk_level);
CREATE INDEX idx_portfolio_risks_latest ON portfolio_risks(portfolio_id, calculation_date DESC, risk_level);
