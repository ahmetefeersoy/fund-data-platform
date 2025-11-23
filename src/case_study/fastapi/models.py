from sqlalchemy import Column, Integer, String , Float , Date , ForeignKey
from sqlalchemy.orm import relationship , declarative_base
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
    
    

def create_tables():
    Base.metadata.create_all(bind=engine)    