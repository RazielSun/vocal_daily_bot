from aiogram import types, Router, F, Bot
from aiogram.types import User
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _


async def send_course(user: User, bot: Bot, i18n: I18n):
    """Send the course message to the user"""
    await bot.send_message(user.id, _("course message"))


router = Router(name="course")


@router.callback_query(F.data == "course")
async def handle_course_menu(callback_query: types.CallbackQuery, i18n: I18n):
    """Handles the /course command"""
    await callback_query.message.edit_reply_markup(
        reply_markup=None
    )  # Remove the inline keyboard
    await send_course(callback_query.from_user, callback_query.bot, i18n)
    await callback_query.answer()
