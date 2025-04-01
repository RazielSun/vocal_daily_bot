import logging
import asyncio
import sys

from bot.core.config import settings
from bot.core.loader import app, bot, dp
from bot.handlers import get_handlers_router
from bot.keyboards.default_commands import remove_default_commands, set_default_commands, set_bot_info

async def on_startup() -> None:
    logging.info("Bot is running...")

    dp.include_router(get_handlers_router())

    await set_default_commands(bot)
    await set_bot_info(bot)

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

async def setup_webhook() -> None:
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
    from aiohttp.web import AppRunner, TCPSite

    logging.info(f"webhook: {settings.webhook_url}")

    await bot.set_webhook(
        settings.webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        secret_token=settings.WEBHOOK_SECRET,
    )

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, host=settings.WEBHOOK_HOST, port=settings.WEBHOOK_PORT)
    await site.start()

    await asyncio.Event().wait()

async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if settings.USE_WEBHOOK:
        await setup_webhook()
    else:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    # Enable logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Run Bot
    asyncio.run(main())