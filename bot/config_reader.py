from enum import Enum

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlalchemy import URL


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")


class FSMModeEnum(str, Enum):
    MEMORY = "memory"
    REDIS = "redis"


class RedisConfig(BaseSettings, env_prefix="REDIS_"):
    host: str
    port: int
    db: int


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    host: str
    db: str
    password: SecretStr
    port: int
    user: str

    def dsn(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )


class BotConfig(BaseSettings, env_prefix="BOT_"):
    token: SecretStr
    forum_supergroup_id: int
    ignored_topics_ids: list[int]
    fsm_mode: FSMModeEnum
    language: str
    albums_preserve_enabled: bool = False
    albums_wait_time_seconds: int = 3.0


class AppConfig(BaseModel):
    bot: BotConfig
    postgres: PostgresConfig
    redis: RedisConfig


def create_app_config() -> AppConfig:
    return AppConfig(
        bot=BotConfig(),
        postgres=PostgresConfig(),
        redis=RedisConfig(),
    )
