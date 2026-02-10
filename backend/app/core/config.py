from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "dev"
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    AMAZON_MODE: str = "mock"  # mock|live
    AMAZON_ASSOCIATE_TAG: str = "demo-20"
    AMAZON_ACCESS_KEY: str | None = None
    AMAZON_SECRET_KEY: str | None = None
    AMAZON_REGION: str = "us-east-1"

    PUBLIC_BASE_URL: str = "http://localhost:8000"

settings = Settings()
