# Architecture

The platform is organized around ingestion, retrieval, analysis agents, valuation, and report generation.

1. Ingestion services collect SEC filings, earnings transcripts, and news.
2. PostgreSQL stores normalized company, filing, transcript, and report metadata.
3. Pinecone stores source chunks and embeddings for semantic and hybrid retrieval.
4. FastAPI exposes research, filing, company, report, and workflow APIs.
5. LangGraph coordinates financial, risk, sentiment, competitor, valuation, and recommendation agents.
6. React renders analyst workflows, company pages, DCF summaries, and institutional reports.
