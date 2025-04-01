import os
import argparse
import csv
import json
from pathlib import Path

# Paths relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent  # points to root/

SOURCE_DIR = BASE_DIR / "sources"
LOCALES_DIR = BASE_DIR / "bot" / "locales"

LANGS = ["en", "ru"]
SPREADSHEET_NAME = "Vocal Bot Strings"
CORE_SHEET = "BotCore"
# DAILY_SHEET = "Daily"


def init_args():
    parser = argparse.ArgumentParser(description="Manage content data.")
    parser.add_argument(
        "--sources", action="store_true", help="Extract from csv sources."
    )
    return parser.parse_args()


def get_data_from_sources(spreadsheet, sheetname, func):

    core_name = spreadsheet + " - " + sheetname + ".csv"
    with open(SOURCE_DIR / core_name, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        result = func(reader)

    return result


def parse_core_data(data):
    result = {}
    for row in data:
        name_id = row["name_id"]
        if name_id == "":
            continue
        langs = {}
        for k in LANGS:
            lang_key = f"text_{k}"
            langs[k] = row[lang_key]
        result[name_id] = langs
    return result


def update_core_files():
    table_data = get_data_from_sources(SPREADSHEET_NAME, CORE_SHEET, parse_core_data)

    os.makedirs(LOCALES_DIR, exist_ok=True)

    default_commands = {}
    descriptions = {}
    for k, v in table_data.items():
        if k.startswith("bot_"):
            descriptions[k] = v
        else:
            default_commands[k] = v

    filepath = os.path.join(LOCALES_DIR, f"default_commands.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(default_commands, f, ensure_ascii=False, indent=2)

    filepath = os.path.join(LOCALES_DIR, f"descriptions.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(descriptions, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    args = init_args()

    update_core_files()
