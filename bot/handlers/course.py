from aiogram import types, Router, F
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

router = Router(name="course")

@router.callback_query(F.data == "course")
async def handle_course_menu(callback_query: types.CallbackQuery, i18n: I18n):
    """Handles the /course command"""
    await callback_query.message.edit_reply_markup(reply_markup=None) # Remove the inline keyboard
    # await message.bot.send_message(_("course message"))
    await callback_query.answer()