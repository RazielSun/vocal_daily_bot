from aiogram import types, Router, F, Bot
from aiogram.types.user import User
from aiogram.filters import Command
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _


async def send_training(user: User, bot: Bot, i18n: I18n):
    """Send the training in sequence."""
    await bot.send_message(user.id, _("training message"))


router = Router(name="training")


@router.callback_query(F.data == "training")
async def handle_training_menu(callback_query: types.CallbackQuery, i18n: I18n):
    """Handles the training in menu"""
    await callback_query.message.edit_reply_markup(reply_markup=None) # Remove the inline keyboard
    await send_training(callback_query.from_user, callback_query.bot, i18n)
    await callback_query.answer()
