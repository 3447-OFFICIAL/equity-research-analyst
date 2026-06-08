from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://equity:equity@localhost:5432/equity_research"
    pinecone_api_key: str | None = None
    pinecone_index: str = "equity-research"
    openai_api_key: str | None = None
    sec_user_agent: str = Field(default="AI Equity Research Analyst contact@example.com")
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
