from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"
    db_name: str = "contractlens"
    reset_token_secret: str = "fallback_secret"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    domain: str = "http://localhost:8000"


class TemplateSettings:
    TEMPLATE_DIR = BASE_DIR / "templates/pages"
    STATIC_DIR = BASE_DIR / "static"
    STATIC_URL = "/static"
    STATIC_NAME = "static"


template_settings = TemplateSettings()
settings = Settings()
