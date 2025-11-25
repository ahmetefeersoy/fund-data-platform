from sqlalchemy import Column, Integer, String , Float , Date , ForeignKey, Boolean, Numeric, DateTime
from sqlalchemy.orm import relationship , declarative_base
from sqlalchemy.sql import func
from src.case_study.utils.db import engine

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = 'portfolios'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    
    positions = relationship("Position", back_populates="portfolio", cascade="all, delete-orphan")

    

class Position(Base):
    __tablename__ = 'positions'
    
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    fund_code = Column(String, index=True, nullable=False)
    weight  = Column(Float, nullable=False)
    purchase_date = Column(Date)
    purchase_price = Column(Float)
    portfolio = relationship("Portfolio", back_populates="positions")


class PortfolioRisk(Base):
    __tablename__ = 'portfolio_risks'
    
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, nullable=False, index=True)
    calculation_date = Column(Date, nullable=False, index=True)
    risk_score = Column(Numeric, nullable=False)
    risk_level = Column(String, nullable=False)
    volatility = Column(Numeric)
    sharpe_ratio = Column(Numeric)
    max_drawdown = Column(Numeric)
    var_95 = Column(Numeric)
    days_analyzed = Column(Integer)
    created_at = Column(DateTime, server_default=func.current_timestamp())


class FundPerformance(Base):
    __tablename__ = 'fund_performance'
    
    id = Column(Integer, primary_key=True, index=True)
    fund_code = Column(String, nullable=False, index=True)
    calculation_date = Column(Date, nullable=False, index=True)
    performance_score = Column(Numeric, nullable=False)
    returns_30d = Column(Numeric)
    returns_90d = Column(Numeric)
    returns_180d = Column(Numeric)
    category_avg_return = Column(Numeric)
    category_rank = Column(Integer)
    total_peers = Column(Integer)
    is_underperforming = Column(Boolean, default=False, index=True)
    confidence_score = Column(Numeric)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    

def create_tables():
    Base.metadata.create_all(bind=engine)    