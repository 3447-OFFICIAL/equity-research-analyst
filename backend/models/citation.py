from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from backend.models.company import Base

class Citation(Base):
    __tablename__ = "citations"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, index=True) # Would reference reports.id
    claim_text = Column(Text, nullable=False)
    source_document = Column(String(128))
    section_name = Column(String(128))
    chunk_id = Column(String(255), index=True)
    confidence = Column(Numeric, nullable=True)
