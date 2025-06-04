
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, EmailStr

# Calculate absolute path to .env file located at the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):
    testing: bool = False

    DATABASE_URL: str = Field(...)
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = Field(...)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(...)
    GEMINI_API_KEY: str = Field(...)

    # Mail (SMTP) settings for password reset emails
    MAIL_SERVER: str = Field(...)
    MAIL_PORT: int = Field(...)
    MAIL_USERNAME: str = Field(...)
    MAIL_PASSWORD: str = Field(...)
    MAIL_FROM: EmailStr = Field(...)
    MAIL_STARTTLS:bool
    MAIL_SSL_TLS:bool

    #Add this for Firebase integration
    GOOGLE_APPLICATION_CREDENTIALS: str
    #the name of the App
    TITLE:str 
    VERSION:str
    # #for Celery
    # CELERY_BROKER_URL: str
    # CELERY_RESULT_BACKEND:str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra="ignore",
        populate_by_name=True
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()