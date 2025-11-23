from src.case_study.utils.db import engine
from src.case_study.fastapi.models import Base

from sqlalchemy.orm import Session
from . import models, schemas

def create_tables():
    Base.metadata.create_all(bind=engine)
    
    
def create_user_portfolio(db: Session, portfolio: schemas.PortfolioCreate):
    user_portfolio = models.Portfolio(name=portfolio.name, description=portfolio.description)
    db.add(user_portfolio)
    db.flush()  
    
    for pos in portfolio.positions:
        db_position = models.Position(
            fund_code=pos.fund_code,
            weight=pos.weight,
            purchase_date=pos.purchase_date,
            purchase_price=pos.purchase_price,
            portfolio_id=user_portfolio.id
        )
        db.add(db_position)
        
    db.commit()
    db.refresh(user_portfolio)
    return user_portfolio    

def get_user_portfolios(db: Session):
    return db.query(models.Portfolio).all()

def get_user_portfolio(db: Session, portfolio_id: int):
    return db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()

def update_user_portfolio(db: Session, portfolio_id: int, portfolio_update: schemas.PortfolioUpdate):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not portfolio:
        return None
    
    if portfolio_update.name is not None:
        portfolio.name = portfolio_update.name
        
    if portfolio_update.description is not None:
        portfolio.description = portfolio_update.description
        
    db.query(models.Position).filter(models.Position.portfolio_id == portfolio.id).delete()    
    
    for pos in portfolio_update.positions:
        db.add(models.Position(
            fund_code=pos.fund_code,
            weight=pos.weight,
            purchase_date=pos.purchase_date,
            purchase_price=pos.purchase_price,
            portfolio_id=portfolio.id
        ))
    
    db.commit()
    db.refresh(portfolio)
    return portfolio

def delete_user_portfolio(db: Session, portfolio_id: int):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not portfolio:
        return None
    
    db.delete(portfolio)
    db.commit()
    return portfolio