from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from backend.models.company import Base

class FinancialMetric(Base):
    __tablename__ = "financial_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    metric_name = Column(String(128), nullable=False, index=True) # e.g. Revenue, NetIncome
    value = Column(Numeric, nullable=False)
    period_end_date = Column(Date, nullable=False)
    filing_type = Column(String(10), nullable=False) # 10-K, 10-Q
    source = Column(String(64), nullable=False) # SEC_XBRL, FMP, etc.
