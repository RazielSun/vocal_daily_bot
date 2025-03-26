import os
import subprocess
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

if __name__ == "__main__":
    # extract_messages()
    # init_locale("en")
    # init_locale("ru")
    # init_locale("es")
    # update_translations()
    compile_translations()
