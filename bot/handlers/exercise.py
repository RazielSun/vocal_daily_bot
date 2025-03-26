import json

from aiogram import Bot, types, Router, F
from aiogram.types import FSInputFile, User
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

from bot.utils.user_progress import get_progress, inc_progress, reset_progress
from bot.core.config import DATA_DIR

router = Router(name="daily")

with open(f"{DATA_DIR}/sequences.json", "r", encoding="utf-8") as file:
    SEQUENCES = json.load(file)
    SEQUENCE = SEQUENCES[0] # validate len

async def send_start_exercise(user: User, bot: Bot, i18n: I18n):
    """Send the next exercise in sequence."""
    reset_progress(user.id)
    await send_next_exercise(user, bot, i18n)

async def send_next_exercise(user: User, bot: Bot, i18n: I18n):
    """Send the next exercise in sequence."""
    progress = get_progress(user.id)
    step = progress["step"]

    exercise_message = _("🎶 Exercise %(step)d:") % { "step": step + 1 }
    await bot.send_message(user.id, exercise_message)

    total_exercises = len(SEQUENCE['sequence'])
    if step < total_exercises:
        exercise_path = f"{SEQUENCE['sequence'][step]}.json"
        with open(exercise_path, "r", encoding="utf-8") as exfile:
            EXERCISE = json.load(exfile)

        await bot.send_message(user.id, _(f"{EXERCISE['description']}"))

        # Send audio if available
        if EXERCISE["audio"]:
            audio_file = FSInputFile(EXERCISE["audio"])
            await bot.send_audio(user.id, audio_file)

        # Move to the next exercise
        inc_progress(user.id)

        # If it's the last in sequence, show the final exercise button
        if step == total_exercises - 1:
            await bot.send_message(user.id, _("final exercise is done")) #, reply_markup=final_exercise_button) # "✅ Click below for the final exercise!"
        else:
            from bot.keyboards.inline import next_exercise_button
            await bot.send_message(user.id, _("click next exercise:"), reply_markup=next_exercise_button(i18n)) #"⏭ Click below for the next exercise:"
    # else:
    #     from handlers.final import send_final_exercise
    #     await send_final_exercise(user_id, bot)

@router.callback_query(F.data == "start_exercise")
async def handle_start_exercise(callback_query: types.CallbackQuery, i18n: I18n):
    """Handles the button click for start exercise"""
    await send_start_exercise(callback_query.from_user, callback_query.bot, i18n)
    await callback_query.answer()

@router.callback_query(F.data == "next_exercise")
async def handle_next_exercise(callback_query: types.CallbackQuery, i18n: I18n):
    """Handles the button click for next exercise"""
    await send_next_exercise(callback_query.from_user, callback_query.bot, i18n)
    await callback_query.answer()
