from aiogram import Bot, types, Router
from aiogram.types.user import User
from aiogram.filters import Command, CommandStart
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline.menu import main_keyboard

router = Router(name="start")

@router.message(CommandStart())
async def start_command(message: types.Message, i18n: I18n):
    """Handles the /start command and begins the daily training session."""
    await message.answer(_("welcome message"), reply_markup=main_keyboard())
