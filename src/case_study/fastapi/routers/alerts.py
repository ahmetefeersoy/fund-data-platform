from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...utils.db import SessionLocal
from .. import controllers, schemas

router = APIRouter(prefix="/alerts", tags=["Alerts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/portfolios", response_model=list[schemas.PortfolioAlertResponse])
async def get_high_risk_portfolios(db: Session = Depends(get_db)):
    high_risk_portfolios = controllers.get_high_risk_portfolios(db)
    
    return [
        schemas.PortfolioAlertResponse(
            portfolio_id=risk.portfolio_id,
            risk_score=float(risk.risk_score),
            risk=risk.risk_level
        )
        for risk in high_risk_portfolios
    ]


@router.get("/funds", response_model=list[schemas.FundAlertResponse])
async def get_underperforming_funds(db: Session = Depends(get_db)):
    underperformers = controllers.get_underperforming_funds(db)
    
    return [
        schemas.FundAlertResponse(
            fund_code=fund.fund_code,
            confidence=float(fund.confidence_score)
        )
        for fund in underperformers
    ]
