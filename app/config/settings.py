import os
import sys
from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class EnvironmentEnum(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    LOCAL = "local"


class GlobalConfig(BaseSettings):
    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    TESTING: bool = False
    TIMEZONE: str = "UTC"

    DB_ECHO_LOG: bool = False

    MIN_CODE_LENGTH_WITHOUT_PREFIX: int = 8
    MAX_CODE_LENGTH_WITHOUT_PREFIX: int = 12

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'


class CloudConfig(GlobalConfig):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str = "discount-service"

    @property
    def sqlalchemy_database_url(self):
        return (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def async_database_url(self) -> Optional[str]:
        return (
            self.sqlalchemy_database_url.replace("postgresql://", "postgresql+asyncpg://")
            if self.sqlalchemy_database_url
            else self.sqlalchemy_database_url
        )


class LocalConfig(GlobalConfig):
    """
    Local configurations
    """

    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL

    @property
    def sqlalchemy_database_url(self):
        if self.TESTING:
            return "sqlite:///./test.db"

        return "sqlite:///./local.db"

    @property
    def async_database_url(self) -> Optional[str]:
        return self.sqlalchemy_database_url.replace("sqlite", "sqlite+aiosqlite")


class StagingConfig(CloudConfig):
    """
    Staging configurations
    """

    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.STAGING


class ProdConfig(CloudConfig):
    """
    Production configurations
    """

    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION


config_mapper = {"local": LocalConfig, "staging": StagingConfig, "production": ProdConfig}


@lru_cache()
def get_configuration() -> GlobalConfig:
    if 'pytest' in sys.modules or 'py.test' in sys.modules:
        config_class = LocalConfig()
        config_class.TESTING = True
        return config_class

    config_class = config_mapper.get(os.getenv("ENVIRONMENT", "production"))()
    return config_class


settings = get_configuration()
