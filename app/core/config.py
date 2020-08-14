import os
import secrets
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    CODE_PATH: Path = Path(__file__).parents[2]

    SERVICE_NAME: Optional[str] = "fastapi-template"

    @validator("SERVICE_NAME", pre=True)
    def get_service_name(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        from app.utils.lifecycle import get_version_and_service_name

        _, service_name = get_version_and_service_name()

        return service_name

    TESTING: Optional[bool] = False

    DDL_PATH: Path = CODE_PATH / "app" / "infrastructure" / "database" / "migrations"
    MODELS_PATH: Path = CODE_PATH / "app" / "infrastructure" / "database" / "models"

    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    DB_NAME_TEST: Optional[str] = None

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.TESTING:
            db_name = f"{self.DB_NAME_TEST}"
        else:
            db_name = f"{self.DB_NAME}"

        return f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{db_name}?application_name={self.SERVICE_NAME}"

    SENTRY_DSN: Optional[str] = None

    class Config:
        env_file = ".env"  # p: Path = Path(__file__).parents[2] / ".env"
        case_sensitive = True


settings = Settings()
