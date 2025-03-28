import json
import logging

from aiogram import Bot, types, Router, F
from aiogram.types import FSInputFile, User
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

from bot.utils.user_progress import get_progress, update_progress, reset_progress
from bot.core.config import CONTENT_DIR
from bot.keyboards.inline import next_exercise_button

router = Router(name="daily")

EXERCISES_DIR = f"{CONTENT_DIR}/exercises"
DAILY_FILE = f"{CONTENT_DIR}/daily.json"

with open(DAILY_FILE, "r", encoding="utf-8") as file:
    DAILY_TRAINS = json.load(file)
    DAILY_TRAIN = DAILY_TRAINS[0]  # TODO: validate len, randomize

def _cstmgettext(text: dict, user: User) -> str:
    _lang = user.language_code if user.language_code in text else "en"
    if _lang in text:
        return text[_lang]
    return text.get("en", "NO TRANSLATION")


async def send_start_exercise(user: User, bot: Bot, i18n: I18n):
    """Send the next exercise in sequence."""
    reset_progress(user.id)
    await send_next_exercise(user, bot, i18n)


async def send_next_exercise(user: User, bot: Bot, i18n: I18n):
    """Send the next exercise in sequence."""
    progress = get_progress(user.id)
    ex_idx = progress["exercise"]
    step_idx = progress["step"]

    # logging.info(f"User {user.id} - Exercise {ex_idx} - Step {step_idx}")

    if ex_idx == 0 and step_idx == 0:
        await bot.send_message(user.id, _cstmgettext(DAILY_TRAIN["text"], user))

    total_exercises = len(DAILY_TRAIN["exercises"])
    if ex_idx < total_exercises:
        with open(DAILY_TRAIN["exercises"][ex_idx], "r", encoding="utf-8") as exfile:
            exercise_data = json.load(exfile)
        
        total_steps = len(exercise_data["steps"])
        
        while step_idx < total_steps:
            step_data = exercise_data["steps"][step_idx]
            step_idx += 1

            need_wait = not step_data["no_wait"]

            last_exercise = ex_idx == total_exercises - 1 and step_idx == total_steps
            reply_markup = (need_wait and not last_exercise) and next_exercise_button(i18n) or None
        
            message = _cstmgettext(step_data["text"], user)
            if step_data["audio"]:
                await bot.send_audio(user.id, step_data["audio"], caption=message, reply_markup=reply_markup)
            elif step_data["image"]:
                pass
            else:
                await bot.send_message(user.id, message, reply_markup=reply_markup)
            
            if need_wait:
                break;
            

        if step_idx == total_steps:
            ex_idx += 1
            step_idx = 0

        update_progress(user.id, ex_idx, step_idx)
            
        # If it's the last in sequence, show the final exercise button
        # if step == total_exercises - 1:
        #     await bot.send_message(
        #         user.id, _("final exercise is done")
        #     )  # , reply_markup=final_exercise_button) # "✅ Click below for the final exercise!"
        # else:
        #     from bot.keyboards.inline import next_exercise_button

        #     await bot.send_message(
        #         user.id,
        #         _("click next exercise:"),
        #         reply_markup=next_exercise_button(i18n),
        #     )  # "⏭ Click below for the next exercise:"
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
