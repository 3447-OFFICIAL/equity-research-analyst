CREATE TABLE IF NOT EXISTS companies (
    id BIGSERIAL PRIMARY KEY,
    ticker VARCHAR(16) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS filings (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES companies(id),
    accession_number VARCHAR(64) UNIQUE,
    form_type VARCHAR(16) NOT NULL,
    filing_date DATE,
    revenue NUMERIC,
    net_income NUMERIC,
    risk_factors TEXT,
    mda TEXT,
    raw_source_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transcript_chunks (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    transcript_date DATE,
    speaker VARCHAR(255),
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding_id VARCHAR(255),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_filings_company_form ON filings(company_id, form_type);
CREATE INDEX IF NOT EXISTS idx_transcript_chunks_company ON transcript_chunks(company_id);
