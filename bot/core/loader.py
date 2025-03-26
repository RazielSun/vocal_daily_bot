from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
# from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware
# from aiohttp import web

from .config import DEFAULT_LOCALE, I18N_DOMAIN, LOCALES_DIR, BOT_TOKEN

# This is forom bot template
# app = web.Application()
# bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

# storage = RedisStorage(
#     redis=redis_client,
#     key_builder=DefaultKeyBuilder(with_bot_id=True),
# )

# dp = Dispatcher(storage=storage)

i18n: I18n = I18n(path=LOCALES_DIR, default_locale=DEFAULT_LOCALE, domain=I18N_DOMAIN)
SimpleI18nMiddleware(i18n).setup(dp)