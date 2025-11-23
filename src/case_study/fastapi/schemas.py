from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class PositionBase(BaseModel):
    fund_code: str = Field(..., description="Fon kodu")
    weight: float = Field(..., ge=0, le=100, description="Ağırlık (0-100)")
    purchase_date: Optional[date] = Field(None, description="Alış tarihi")
    purchase_price: Optional[float] = Field(None, ge=0, description="Alış fiyatı")


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    fund_code: Optional[str] = None
    weight: Optional[float] = Field(None, ge=0, le=100)
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = Field(None, ge=0)


class Position(PositionBase):
    id: int
    portfolio_id: int
    
    class Config:
        from_attributes = True


class PortfolioBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Portfolio adı")
    description: Optional[str] = Field(None, description="Portfolio açıklaması")


class PortfolioCreate(PortfolioBase):
    positions: Optional[List[PositionCreate]] = Field(default_factory=list)


class PortfolioUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class Portfolio(PortfolioBase):
    id: int
    positions: List[Position] = []
    
    class Config:
        from_attributes = True
