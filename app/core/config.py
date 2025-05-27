# from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import Field
# from functools import lru_cache


# class Settings(BaseSettings):
#     app_name: str = "Resume AI Generator"
#     environment: str = "development"
#     testing: bool = False
#     DATABASE_URL: str = Field()
#     SECRET_KEY: str = Field()
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#     GEMINI_API_KEY: str = Field()

#     model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)


# @lru_cache()
# def get_settings():
#     return Settings()


# settings = get_settings()











# from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import Field
# from functools import lru_cache


# class Settings(BaseSettings):
#     app_name: str = "Resume AI Generator"
#     environment: str = "development"
#     testing: bool = False

#     DATABASE_URL: str = Field()
#     SECRET_KEY: str = Field()
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#     GEMINI_API_KEY: str = Field()

#     # Add this for Firebase integration
#     GOOGLE_APPLICATION_CREDENTIALS: str = Field()

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         extra="ignore",
#         populate_by_name=True
#     )


# @lru_cache()
# def get_settings():
#     return Settings()


# settings = get_settings()







import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, EmailStr

# Calculate absolute path to .env file located at the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):
    app_name: str = "Resume AI Generator"
    environment: str = "development"
    testing: bool = False

    DATABASE_URL: str = Field(...)
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str = Field(...)

    # Mail (SMTP) settings for password reset emails
    MAIL_SERVER: str = Field(...)
    MAIL_PORT: int = Field(...)
    MAIL_USERNAME: str = Field(...)
    MAIL_PASSWORD: str = Field(...)
    MAIL_FROM: EmailStr = Field(...)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra="ignore",
        populate_by_name=True
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()