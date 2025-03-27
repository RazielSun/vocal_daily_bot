from aiogram import Router

# Admin handlers
# import bot.handlers.admin

def get_handlers_router() -> Router:
    from . import start, exercise

    router = Router()
    router.include_router(start.router)
    router.include_router(exercise.router)

    return router