from __future__ import annotations
import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import TYPE_CHECKING

DIR = Path(__file__).absolute().parent.parent.parent
CONTENT_DIR = f"{DIR}/content"
BOT_DIR = Path(__file__).absolute().parent.parent
LOCALES_DIR = f"{BOT_DIR}/locales"
I18N_DOMAIN = "messages"
DEFAULT_LOCALE = "en"

class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

class WebhookSettings(EnvBaseSettings):
    USE_WEBHOOK: bool = False
    WEBHOOK_BASE_URL: str = "https://xxx.ngrok-free.app"
    WEBHOOK_PATH: str = "/webhook"
    WEBHOOK_SECRET: str = ""
    WEBHOOK_HOST: str = "localhost"
    WEBHOOK_PORT: int = 8080

    @property
    def webhook_url(self) -> str:
        if settings.USE_WEBHOOK:
            return f"{self.WEBHOOK_BASE_URL}{self.WEBHOOK_PATH}"
        return f"http://localhost:{settings.WEBHOOK_PORT}{settings.WEBHOOK_PATH}"

class BotSettings(WebhookSettings):
    BOT_TOKEN: str = Field(alias='TELEGRAM_BOT_TOKEN')
    SUPPORT_URL: str | None = None
    RATE_LIMIT: int | float = 0.5  # for throttling control

class Settings(BotSettings):
    DEBUG: bool = False

settings = Settings()