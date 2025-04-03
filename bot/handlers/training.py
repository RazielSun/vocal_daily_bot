import json
import logging

from aiogram import types, Router, F, Bot
from aiogram.types.user import User
from aiogram.filters import Command
from aiogram.utils.i18n.core import I18n
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline.daily_buttons import exercises_list_buttons, next_training_button
from bot.filters.callbacks import TrainingCallbackData
from bot.core.content import cstmgettext as _cstmgettext, get_training, load_exercise


async def send_training(user: User, bot: Bot, i18n: I18n):
    """Send the training in sequence."""
    await bot.send_message(
        user.id, _("training message"), reply_markup=exercises_list_buttons()
    )


async def select_training(user: User, bot: Bot, callback_data: TrainingCallbackData, i18n: I18n):
    """Send the next exercise in sequence."""
    if callback_data.index == -1:
        await bot.send_message(user.id, _("invalid index"))
        return
    
    training_id = callback_data.index
    practice = get_training(training_id)
    if not practice:
        await bot.send_message(user.id, _("invalid training"))
        return

    ex_idx = callback_data.exercise_id
    step_idx = callback_data.step_id

    # logging.info(f"[DEBUG] User {user.id} - Exercise {ex_idx} - Step {step_idx}")

    if ex_idx == -1 and step_idx == -1:
        await bot.send_message(
            user.id,
            _cstmgettext(practice["text"], user),
            reply_markup=next_training_button(training_id, 0, 0, i18n),
        )
        return

    total_exercises = len(practice["exercises"])
    if ex_idx < total_exercises:
        exercise_data = load_exercise(practice["exercises"][ex_idx])
        total_steps = len(exercise_data["steps"])

        while step_idx < total_steps:
            step_data = exercise_data["steps"][step_idx]
            need_wait = not step_data["no_wait"]

            message = _cstmgettext(step_data["text"], user)
            formatted_msg = (
                step_idx == 0
                and _("exercise %d: %s") % (ex_idx + 1, message)
                or message
            )

            step_idx += 1
            # logging.info(f"[DEBUG] Update User {user.id} - Exercise {ex_idx} - Step {step_idx}")

            last_exercise = (
                ex_idx == total_exercises - 1 and step_idx == total_steps
            )

            next_ex_idx = ex_idx
            next_step_idx = step_idx
            if next_step_idx == total_steps:
                next_ex_idx += 1
                next_step_idx = 0
                # logging.info(f"[DEBUG] Next User {user.id} - Exercise {next_ex_idx} - Step {next_step_idx}")

            reply_markup = (
                (need_wait and not last_exercise) and next_training_button(training_id, next_ex_idx, next_step_idx, i18n) or None
            )

            if step_data["audio"]:
                await bot.send_audio(
                    user.id,
                    step_data["audio"],
                    caption=formatted_msg,
                    reply_markup=reply_markup,
                )
            elif step_data["image"]:
                await bot.send_photo(
                    user.id,
                    step_data["image"],
                    caption=formatted_msg,
                    reply_markup=reply_markup,
                )
            else:
                await bot.send_message(
                    user.id, formatted_msg, reply_markup=reply_markup
                )

            if need_wait:
                break


router = Router(name="training")


@router.callback_query(F.data == "training")
async def handle_training_menu(callback_query: types.CallbackQuery, i18n: I18n):
    """Handles the training in menu"""
    await callback_query.message.edit_reply_markup(
        reply_markup=None
    )  # Remove the inline keyboard
    await send_training(callback_query.from_user, callback_query.bot, i18n)
    await callback_query.answer()


@router.callback_query(TrainingCallbackData.filter())
async def handle_select_training_menu(callback_query: types.CallbackQuery, callback_data: TrainingCallbackData, i18n: I18n):
    """Handles the select training in training menu"""
    if callback_data.action != "select":
        return
    await callback_query.message.edit_reply_markup(
        reply_markup=None
    )  # Remove the inline keyboard
    await select_training(callback_query.from_user, callback_query.bot, callback_data, i18n)
    await callback_query.answer()
