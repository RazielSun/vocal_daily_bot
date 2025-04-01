from __future__ import annotations
import json
from typing import TYPE_CHECKING

from aiogram.types import BotCommand, BotCommandScopeDefault

if TYPE_CHECKING:
    from aiogram import Bot

from bot.core.config import LOCALES_DIR

with open(f"{LOCALES_DIR}/default_commands.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)
    users_commands = {}
    for command, langs in raw_data.items():
        for language_code, description in langs.items():
            if users_commands.get(language_code) is None:
                users_commands[language_code] = {}
            users_commands[language_code][command] = description


async def set_default_commands(bot: Bot) -> None:
    await remove_default_commands(bot)

    for language_code, commands in users_commands.items():
        await bot.set_my_commands(
            [BotCommand(command=command, description=description) for command, description in commands.items()],
            scope=BotCommandScopeDefault(),
            language_code=language_code,
        )


async def remove_default_commands(bot: Bot) -> None:
    await bot.delete_my_commands(scope=BotCommandScopeDefault())


with open(f"{LOCALES_DIR}/descriptions.json", "r", encoding="utf-8") as f:
    descriptions = json.load(f)


async def set_bot_info(bot: Bot) -> None:
    for key, langs in descriptions.items():
        for language_code, data in langs.items():
            if key == "bot_about":
                await bot.set_my_short_description(
                    short_description=data, language_code=language_code
                )
            elif key == "bot_description":
                await bot.set_my_description(
                    description=data, language_code=language_code
                )
