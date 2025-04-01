from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.config import settings

def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [InlineKeyboardButton(text=_("daily button"), callback_data="daily")],
        [InlineKeyboardButton(text=_("training button"), callback_data="training")],
        [InlineKeyboardButton(text=_("course button"), callback_data="course")],
        [InlineKeyboardButton(text=_("info button"), callback_data="info")],
        [InlineKeyboardButton(text=_("support button"), url=settings.SUPPORT_URL)],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1, 2, 2)

    return keyboard.as_markup()