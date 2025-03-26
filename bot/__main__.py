import logging
import asyncio
import sys

from bot.handlers import get_handlers_router
from bot.keyboards.default_commands import remove_default_commands, set_default_commands
from bot.core.loader import bot, dp

async def on_startup() -> None:
    logging.info("Bot is running...")

    dp.include_router(get_handlers_router())

    await set_default_commands(bot)

    bot_info = await bot.get_me()

    logging.info(f"Name     - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID       - {bot_info.id}")

    logging.info("Bot started")

async def on_shutdown() -> None:
    logging.info("bot stopping...")

    await remove_default_commands(bot)

    # await dp.storage.close()
    # await dp.fsm.storage.close()

    logging.info("Bot stopped")

async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)

if __name__ == "__main__":
    # Enable logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Run Bot
    asyncio.run(main())