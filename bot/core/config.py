from __future__ import annotations
import os
from pathlib import Path
from typing import TYPE_CHECKING

DIR = Path(__file__).absolute().parent.parent.parent
DATA_DIR = f"{DIR}/data"
BOT_DIR = Path(__file__).absolute().parent.parent
LOCALES_DIR = f"{BOT_DIR}/locales"
I18N_DOMAIN = "messages"
DEFAULT_LOCALE = "en"

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")