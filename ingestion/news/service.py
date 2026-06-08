class NewsIngestionService:
    def ingest_company_news(self, ticker: str) -> list[dict[str, object]]:
        raise NotImplementedError("News ingestion will be implemented in a later phase.")
