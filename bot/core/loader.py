from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware
from aiohttp import web

from .config import DEFAULT_LOCALE, I18N_DOMAIN, LOCALES_DIR, settings

app = web.Application()

token = settings.BOT_TOKEN

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

i18n: I18n = I18n(path=LOCALES_DIR, default_locale=DEFAULT_LOCALE, domain=I18N_DOMAIN)
SimpleI18nMiddleware(i18n).setup(dp)

DEBUG = settings.DEBUG