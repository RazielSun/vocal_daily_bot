import json

# Load translations from the JSON file
with open("data/translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)


def gettext(key: str, lang: str = "en") -> str:
    """
    Retrieve the message for the given language and key.
    Falls back to English if the language or key is missing.
    """
    _lang = lang if lang in translations else "en"
    if _lang in translations and key in translations[_lang]:
        return translations[_lang][key]
    return translations.get("en", {}).get(key, key)
