from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Date, Numeric, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.company import Base


class Filing(Base):
    __tablename__ = "filings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    accession_number: Mapped[str | None] = mapped_column(String(64), unique=True)
    form_type: Mapped[str] = mapped_column(String(16), nullable=False)
    filing_date: Mapped[date | None] = mapped_column(Date)
    revenue: Mapped[Decimal | None] = mapped_column(Numeric)
    net_income: Mapped[Decimal | None] = mapped_column(Numeric)
    risk_factors: Mapped[str | None] = mapped_column(Text)
    mda: Mapped[str | None] = mapped_column(Text)
    raw_source_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Example relationship
    # company: Mapped["Company"] = relationship("Company", back_populates="filings")
