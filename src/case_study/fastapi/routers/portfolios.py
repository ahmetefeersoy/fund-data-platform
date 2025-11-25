from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...utils.db import engine
from .. import controllers, schemas, models

router = APIRouter(prefix="/portfolios", tags=["Portfolios"])

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
        
# Router for creating
@router.post("/", response_model=schemas.Portfolio)
async def create_portfolio(portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)):
    return controllers.create_user_portfolio(db, portfolio)

# Router for reading all portfolios
@router.get("/", response_model=list[schemas.Portfolio])
async def read_portfolios(db: Session = Depends(get_db)):
    return controllers.get_user_portfolios(db)

# Router for reading a single portfolio
@router.get("/{portfolio_id}", response_model=schemas.Portfolio)
async def read_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    db_portfolio = controllers.get_user_portfolio(db, portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_portfolio

# Router for updating a portfolio
@router.put("/{portfolio_id}", response_model=schemas.Portfolio)
async def update_portfolio(portfolio_id: int, portfolio_update: schemas.PortfolioUpdate,
                            db: Session = Depends(get_db)):
     db_portfolio = controllers.update_user_portfolio(db, portfolio_id, portfolio_update)
     if db_portfolio is None:
          raise HTTPException(status_code=404, detail="Portfolio not found")
     return db_portfolio
 
# Router for deleting a portfolio
@router.delete("/{portfolio_id}", response_model=dict)
async def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    db_portfolio = controllers.get_user_portfolio(db, portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    db.query(models.Position).filter(models.Position.portfolio_id == portfolio_id).delete()
    db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).delete()
    db.commit()
    
    return {"detail": "Portfolio deleted successfully"}


    