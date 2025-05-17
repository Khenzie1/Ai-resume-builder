from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Resume AI Generator"
    environment: str = "development"
    testing: bool = False
    DATABASE_URL: str = Field("sqlite:///./test.db")
    SECRET_KEY: str = Field()
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    GEMINI_API_KEY: str = Field()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
