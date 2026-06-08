from pydantic import BaseModel, Field
from typing import List

class CitationSchema(BaseModel):
    claim: str = Field(..., description="The factual claim made by the analyst.")
    source_document: str = Field(..., description="The name of the document (e.g. 10-K 2025).")
    section: str = Field(..., description="The section name (e.g. Item 7 MD&A).")
    chunk_id: str = Field(..., description="The UUID of the vector chunk in Pinecone.")
    confidence: float = Field(..., description="Agent confidence in this claim (0.0 to 1.0).")

class ClaimResponse(BaseModel):
    claims: List[CitationSchema]

# In a real pipeline, the LLM is forced to output this schema using `with_structured_output`
def verify_citation(citation: CitationSchema) -> bool:
    # Logic to verify chunk_id exists in Pinecone
    # pinecone_index.fetch(ids=[citation.chunk_id])
    return True

def save_citation(db_session, report_id: int, citation: CitationSchema):
    # Logic to save to Postgres
    from backend.models.citation import Citation
    new_citation = Citation(
        report_id=report_id,
        claim_text=citation.claim,
        source_document=citation.source_document,
        section_name=citation.section,
        chunk_id=citation.chunk_id,
        confidence=citation.confidence
    )
    db_session.add(new_citation)
    db_session.commit()
