from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    channel: str
    replenishment: str
    help: str
    reg: str
    postback_password: SecretStr
    database: str
    user: str
    password_db: str
    host: SecretStr
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
