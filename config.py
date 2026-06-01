"""
Application settings loaded from environment variables.
Values are read from a .env file in development; set directly in staging/production.
"""

# import os

# from dotenv import load_dotenv

# load_dotenv()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    app_env: str = "development"
    jwt_expiry_minutes: int = 100
    jwt_algorithm: str
    jwt_secret: str

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()
