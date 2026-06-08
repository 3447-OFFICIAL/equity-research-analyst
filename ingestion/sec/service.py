from dataclasses import dataclass


@dataclass(frozen=True)
class FilingExtraction:
    ticker: str
    form_type: str
    revenue: float | None
    net_income: float | None
    risk_factors: str | None
    mda: str | None


class SECFilingIngestionService:
    def download_10k(self, ticker: str) -> str:
        raise NotImplementedError("SEC filing download will be implemented in Phase 2.")

    def extract_sections(self, filing_text: str, ticker: str) -> FilingExtraction:
        raise NotImplementedError("SEC section extraction will be implemented in Phase 2.")

    def store(self, extraction: FilingExtraction) -> None:
        raise NotImplementedError("PostgreSQL persistence will be implemented in Phase 2.")
