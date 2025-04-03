import json

from aiogram.types import User

from bot.core.config import CONTENT_DIR

EXERCISES_DIR = f"{CONTENT_DIR}/exercises"
TRAININGS_FILE = f"{CONTENT_DIR}/trainings.json"

CACHED_EXERCISES = {}

with open(TRAININGS_FILE, "r", encoding="utf-8") as file:
    TRAININGS_LIST = json.load(file)


def cstmgettext(text: dict, user: User) -> str:
    _lang = user.language_code if user.language_code in text else "en"
    if _lang in text:
        return text[_lang]
    return text.get("en", "NO TRANSLATION")


def get_training(index: int) -> dict:
    """Get the exercise data."""
    if index < 0 or index >= len(TRAININGS_LIST):
        # raise ValueError("Index out of range")
        return None
    return TRAININGS_LIST[index]


def get_training_list() -> list:
    """Get the trainings list."""
    out_array = []
    for i in range(len(TRAININGS_LIST)):
        out_array.append(TRAININGS_LIST[i]["name"])
    return out_array

def load_exercise(path: str) -> dict:
    """Load exercise data from file."""
    if path in CACHED_EXERCISES:
        return CACHED_EXERCISES[path]

    with open(path, "r", encoding="utf-8") as exfile:
        exercise_data = json.load(exfile)

    CACHED_EXERCISES[path] = exercise_data
    return exercise_data