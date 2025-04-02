from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

# "Start Practice ▶️"
def next_exercise_button(i18n: I18n) -> InlineKeyboardMarkup:
    """Use next_exercise_button"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(_("next exercise")), callback_data="next_exercise")]
    ])
