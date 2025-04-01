from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

router = Router(name="training")

@router.callback_query(F.data == "training")
async def start_command(message: types.Message, i18n: I18n):
    """Handles the /training command"""
    await message.bot.send_message(_("training message"))