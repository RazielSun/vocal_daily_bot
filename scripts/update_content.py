import os
import argparse
import csv
import json
from pathlib import Path

# from pydantic_settings import BaseSettings, SettingsConfigDict

# https://stackoverflow.com/questions/27067825/how-to-access-google-spreadsheets-with-a-service-account-credentials
# https://docs.gspread.org/en/v6.1.3/oauth2.html

# Paths relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent  # points to root/
CONTENT_FOLDER = "content"
EXERCISES_FOLDER = "exercises"

SOURCE_DIR = BASE_DIR / "sources"
CONTENT_DIR = BASE_DIR / CONTENT_FOLDER

LANGS = ["en", "ru"]
SPREADSHEET_NAME = "Vocal Exercises Content"
EXERCISES_SHEET = "Exercises"
DAILY_SHEET = "Daily"

# class EnvBaseSettings(BaseSettings):
#     model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", env_file_encoding="utf-8", extra="ignore")

# class GoogleDriveSettings(EnvBaseSettings):
#     # TOKEN: str
#     pass

# settings = GoogleDriveSettings()


def init_args():
    parser = argparse.ArgumentParser(description="Manage content data.")
    parser.add_argument(
        "--sources", action="store_true", help="Extract from csv sources."
    )
    return parser.parse_args()


# for Public sheets
# gc = gspread.api_key("<your newly create key>"")
# sh = gc.open_by_key("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
# print(sh.sheet1.get('A1'))


def auth_client():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        f"{BASE_DIR}/credentials.json", scope
    )
    client = gspread.authorize(creds)
    return client


def get_data_from_gdrive(ex_func, d_func):
    client = auth_client()

    # Exercises
    sheet = client.open(SPREADSHEET_NAME).worksheet(EXERCISES_SHEET)
    ex_result = ex_func(sheet.get_all_records())

    # Daily
    sheet = client.open(SPREADSHEET_NAME).worksheet(DAILY_SHEET)
    d_result = d_func(sheet.get_all_records())

    return ex_result, d_result


def get_data_from_sources(ex_func, d_func):

    ex_name = SPREADSHEET_NAME + " - " + EXERCISES_SHEET + ".csv"
    with open(SOURCE_DIR / ex_name, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        ex_result = ex_func(reader)

    d_name = SPREADSHEET_NAME + " - " + DAILY_SHEET + ".csv"
    with open(SOURCE_DIR / d_name, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        d_result = d_func(reader)

    return ex_result, d_result


def parse_exercises(data):
    exercises = {}
    last_row_id = ""
    for row in data:
        # print(row)
        ex_id = row["id"]
        last_row_id = ex_id if ex_id != "" else last_row_id
        ex_name = row["name"]
        ex_type = row["type"]
        ex_step_id = row["step_id"]
        if ex_step_id == "":
            continue
        ex_audio_id = row["audio_id"]
        ex_image_id = row["image_id"]
        ex_nowait = row["no_wait"]
        langs = {}
        for k in LANGS:
            lang_key = f"text_{k}"
            langs[k] = row[lang_key]
        step = {
            "id": ex_step_id,
            "audio": ex_audio_id != "null" and ex_audio_id or None,
            "image": ex_image_id != "null" and ex_image_id or None,
            "no_wait": ex_nowait == "TRUE" and True or False,
            "text": langs,
        }
        if last_row_id != "" and last_row_id not in exercises:
            exercises[ex_id] = {
                "id": ex_id,
                "name": ex_name,
                "type": ex_type,
                "steps": [],
            }
        exercises[last_row_id]["steps"].append(step)

    return exercises


def parse_daily(data):
    daily = {}
    for row in data:
        d_id = row["id"]
        d_name = row["name"]
        exercises = []
        for i in range(1, 7):
            ex_id = row["exercise_%02d" % i]
            if ex_id != "null":
                exercises.append(ex_id)
        text = {}
        for k in LANGS:
            lang_key = f"text_{k}"
            text[k] = row[lang_key]
        if d_id not in daily:
            daily[d_id] = {
                "id": d_id,
                "name": d_name,
                "exercises": exercises,
                "text": text,
            }

    return daily


def process_content(exercises, daily):
    os.makedirs(CONTENT_DIR, exist_ok=True)
    content_exercises_folder = CONTENT_DIR / EXERCISES_FOLDER
    os.makedirs(content_exercises_folder, exist_ok=True)

    # print(json.dumps(exercises, indent=2))
    for k, v in exercises.items():
        # print(v)
        filename = v["name"]
        filepath = os.path.join(content_exercises_folder, f"{filename}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, indent=2)

    # print(json.dumps(daily, indent=2))
    daily_array = []
    for key, value in daily.items():
        for i in range(len(value["exercises"])):
            value["exercises"][i] = os.path.join(
                CONTENT_FOLDER, EXERCISES_FOLDER, value["exercises"][i] + ".json"
            )
        daily_array.append(value)
    filepath = os.path.join(CONTENT_DIR, "trainings.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(daily_array, f, ensure_ascii=False, indent=2)


def validate_content(exercises, daily):
    result = True
    exercise_names = {}

    for key, value in exercises.items():
        if value["name"] in exercise_names:
            print(f"Exercise {value['name']} already exists.")
            result = False
        exercise_names[value["name"]] = True

    for key, value in daily.items():
        for ex_name in value["exercises"]:
            if ex_name not in exercise_names:
                print(f"Exercise {ex_name} not found in exercises.")
                result = False

    return result


if __name__ == "__main__":
    args = init_args()

    if args.sources:
        exercises, daily = get_data_from_sources(parse_exercises, parse_daily)
    else:
        exercises, daily = get_data_from_gdrive(parse_exercises, parse_daily)

    if validate_content(exercises, daily):
        process_content(exercises, daily)
