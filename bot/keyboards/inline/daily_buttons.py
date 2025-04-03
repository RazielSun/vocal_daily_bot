from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n.core import I18n
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from bot.filters.callbacks import TrainingCallbackData


def next_exercise_button(i18n: I18n) -> InlineKeyboardMarkup:
    """Use next_exercise_button"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=str(_("next exercise")), callback_data="next_exercise"
                )
            ]
        ]
    )


def next_training_button(
    index: int, exercise_id: int, step_id: int, i18n: I18n
) -> InlineKeyboardMarkup:
    """Use next_exercise_button"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=str(_("next exercise")),
                    callback_data=TrainingCallbackData(
                        action="select",
                        index=index,
                        exercise_id=exercise_id,
                        step_id=step_id,
                    ).pack(),
                )
            ]
        ]
    )


def exercises_list_buttons() -> InlineKeyboardMarkup:
    """Use in training menu."""
    from bot.core.content import get_training_list

    data = get_training_list()
    buttons = [
        [
            InlineKeyboardButton(
                text=data[i],
                callback_data=TrainingCallbackData(action="select", index=i).pack(),
            )
            for i in range(len(data))
        ],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    indices = [1 for i in range(len(data))]
    keyboard.adjust(*indices)

    return keyboard.as_markup()
