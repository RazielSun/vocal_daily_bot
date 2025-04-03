from aiogram import Bot, types, Router, F
from aiogram.types import FSInputFile, User
from aiogram.filters import Command
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

from bot.handlers.training import select_training


async def send_start_exercise(user: User, bot: Bot, i18n: I18n):
    """Send the next exercise in sequence."""
    from bot.filters.callbacks import TrainingCallbackData
    # TODO: Write the logic to choose the training for daily practice, not 0
    await select_training(user, bot, TrainingCallbackData(action="select", index=0), i18n)


router = Router(name="daily")


@router.message(Command("daily"))
async def start_command(message: types.Message, i18n: I18n):
    """Handles the /start command and begins the daily training session."""
    await send_start_exercise(message.from_user, message.bot, i18n)


@router.callback_query(F.data == "daily")
async def handle_daily_menu(callback_query: types.CallbackQuery, i18n: I18n):
    """Handles the button click for start exercise"""
    await callback_query.message.edit_reply_markup(
        reply_markup=None
    )  # Remove the inline keyboard
    await send_start_exercise(callback_query.from_user, callback_query.bot, i18n)
    await callback_query.answer()