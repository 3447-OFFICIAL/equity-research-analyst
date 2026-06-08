from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from backend.models.company import Base

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    # user_id = Column(Integer, ForeignKey("users.id")) # Assuming user table exists

class PortfolioAsset(Base):
    __tablename__ = "portfolio_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    ticker = Column(String(10), nullable=False)
    weight = Column(Numeric, nullable=False) # e.g. 0.25 for 25%
