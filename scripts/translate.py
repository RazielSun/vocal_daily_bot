import os
import subprocess
import argparse
from pathlib import Path

# Paths relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent  # points to root/
LOCALES_DIR = BASE_DIR / "bot" / "locales"
SOURCE_DIR = BASE_DIR / "bot"
BABEL_CFG = BASE_DIR / "babel.cfg"
DOMAIN = "messages"
POT_FILE = BASE_DIR / f"{DOMAIN}.pot"

def run(cmd):
    print(f"➤ {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def extract_messages():
    run(f"pybabel extract -F {BABEL_CFG} -o {POT_FILE} {SOURCE_DIR}")

def init_locale(lang):
    run(f"pybabel init -i {POT_FILE} -d {LOCALES_DIR} -l {lang}")

def update_translations():
    run(f"pybabel update -i {POT_FILE} -d {LOCALES_DIR}")

def compile_translations():
    run(f"pybabel compile -d {LOCALES_DIR}")

def init_args():
    parser = argparse.ArgumentParser(description="Manage translation files.")
    parser.add_argument("--extract", action="store_true", help="Extract messages")
    parser.add_argument("--init", action="store_true", help="Update translations")
    parser.add_argument("--update", action="store_true", help="Update translations")
    parser.add_argument("--compile", action="store_true", help="Compile translations")
    return parser.parse_args()

if __name__ == "__main__":
    args = init_args()
    if args.extract:
        extract_messages()
    if args.init:
        init_locale("en")
        init_locale("ru")
        init_locale("es")
    if args.update:
        update_translations()
    if args.compile:
        compile_translations()
