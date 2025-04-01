from aiogram import Router

# Admin handlers
# import bot.handlers.admin

def get_handlers_router() -> Router:
    from . import start, daily, info, course, training

    router = Router()
    router.include_router(start.router)
    router.include_router(daily.router)
    router.include_router(info.router)
    router.include_router(course.router)
    router.include_router(training.router)

    return router