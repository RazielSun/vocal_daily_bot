from aiogram import Bot, types, Router
from aiogram.types.user import User
from aiogram.filters import Command, CommandStart
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline import start_exercise_button

router = Router(name="start")

async def start_exercise(user: User, bot: Bot, i18n: I18n):
    """Send the first exercise in sequence."""
    await bot.send_message(user.id, _("welcome message"), reply_markup=start_exercise_button(i18n))
    # "🎤 Welcome to your Daily Vocal Training! Let's start with the first exercise."

@router.message(CommandStart())
async def start_command(message: types.Message, i18n: I18n):
    """Handles the /start command and begins the daily training session."""
    await start_exercise(message.from_user, message.bot, i18n)

@router.message(Command("about"))
async def start_command(message: types.Message, i18n: I18n):
    """Handles the /about command"""
    await message.bot.send_message(_("about message"))