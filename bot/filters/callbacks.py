from aiogram.filters.callback_data import CallbackData


class TrainingCallbackData(CallbackData, prefix="training_button"):
    action: str = ""
    index: int = -1
    exercise_id: int = -1
    step_id: int = -1
