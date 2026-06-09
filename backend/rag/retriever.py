import uuid
from dataclasses import dataclass, field
from typing import Any
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

from backend.core.config import settings

@dataclass(frozen=True)
class RetrievedDocument:
    id: str
    text: str
    source: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)

class PineconeRetriever:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        # In production, check if index exists first
        # self.index = self.pc.Index(settings.pinecone_index)
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

    async def add_documents(self, texts: list[str], metadatas: list[dict[str, Any]]) -> None:
        if not texts:
            return
        
        vectors = await self.embeddings.aembed_documents(texts)
        records = []
        for text, vector, metadata in zip(texts, vectors, metadatas):
            doc_id = str(uuid.uuid4())
            metadata["text"] = text  # Store text in metadata for retrieval
            records.append((doc_id, vector, metadata))
            
        # self.index.upsert(vectors=records)
        print(f"Mock: Upserted {len(records)} vectors to Pinecone")

    async def retrieve_documents(self, query: str, filters: dict[str, Any] | None = None, top_k: int = 5) -> list[RetrievedDocument]:
        """Retrieve candidate source documents from the vector store."""
        query_vector = await self.embeddings.aembed_query(query)
        
        # mock response since we might not have a real pinecone index
        # response = self.index.query(vector=query_vector, filter=filters, top_k=top_k, include_metadata=True)
        # return [RetrievedDocument(id=m.id, text=m.metadata["text"], source=m.metadata.get("source", ""), score=m.score, metadata=m.metadata) for m in response.matches]
        
        return [
            RetrievedDocument(
                id="mock-123", 
                text="Mock retrieved text related to the query.", 
                source="Mock SEC 10-K", 
                score=0.95
            )
        ]


def rank_documents(query: str, documents: list[RetrievedDocument]) -> list[RetrievedDocument]:
    """Rank retrieved documents for downstream agent context."""
    return sorted(documents, key=lambda document: document.score, reverse=True)


def citation_builder(documents: list[RetrievedDocument]) -> list[dict[str, Any]]:
    """Build structured citations from retrieved source metadata."""
    return [{"id": doc.id, "source": doc.source, "metadata": doc.metadata} for doc in documents]
