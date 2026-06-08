from datetime import date, datetime

from sqlalchemy import BigInteger, Date, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.company import Base


class TranscriptChunk(Base):
    __tablename__ = "transcript_chunks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), index=True)
    transcript_date: Mapped[date | None] = mapped_column(Date)
    speaker: Mapped[str | None] = mapped_column(String(255))
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_id: Mapped[str | None] = mapped_column(String(255))
    metadata: Mapped[dict] = mapped_column(JSONB, server_default='{}')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
