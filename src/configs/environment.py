from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class EnvironmentSettings(BaseSettings):
    bot_token: str = Field(env="BOT_TOKEN")

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

settings = EnvironmentSettings()