from aiogram import types, Router, F, Bot
from aiogram.types.user import User
from aiogram.filters import Command
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _


async def send_info(user: User, bot: Bot, i18n: I18n):
    """Send the next exercise in sequence."""
    await bot.send_message(user.id, _("info message"))


router = Router(name="info")


@router.message(Command("info"))
async def handle_info_command(message: types.Message, i18n: I18n):
    """Handles the /start command and begins the daily training session."""
    await send_info(message.from_user, message.bot, i18n)


@router.callback_query(F.data == "info")
async def handle_info_menu(callback_query: types.CallbackQuery, i18n: I18n):
    """Handles the info from menu"""
    await callback_query.message.edit_reply_markup(reply_markup=None) # Remove the inline keyboard
    await send_info(callback_query.from_user, callback_query.bot, i18n)
    await callback_query.answer()
