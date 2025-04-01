from aiogram import types, Router, F
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

router = Router(name="info")

@router.callback_query(F.data == "info")
async def start_command(message: types.Message, i18n: I18n):
    """Handles the /info command"""
    await message.bot.send_message(_("info message"))
