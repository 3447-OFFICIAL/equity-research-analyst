# AI-Powered Equity Research Analyst

Production-grade skeleton for an AI equity research platform.

## Stack

- FastAPI backend
- React + Tailwind frontend
- PostgreSQL operational store
- Pinecone vector store
- LangGraph multi-agent research workflow

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

Services:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Repository Layout

```text
frontend/    React and Tailwind application
backend/     FastAPI app, agents, RAG, valuation, reports
ingestion/   SEC filings, earnings calls, and news ingestion services
database/    SQL schema and migration seed files
tests/       Backend and integration tests
docs/        Architecture and delivery notes
```
