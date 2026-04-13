from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Retail Analytics API"
    DATABASE_URL: str = "postgresql://analyst:analyst_pass@localhost:5433/retail_analytics"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()