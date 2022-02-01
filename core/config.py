from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: Optional[str] = None
    ADMIN_EMAIL: Optional[str] = None
    ADMIN_PASSWORD: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    # 60 minutes * 24 hours * 30 days = 30 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    class Config:
        env_file = ".env"


# load settings
settings = Settings()
