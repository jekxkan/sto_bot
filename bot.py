import asyncio

from aiogram import Bot, Dispatcher

from src.configs.enviroment import settings
from src.handlers.menu import menu_router
from src.handlers.profile import profile_router

API_TOKEN = settings.bot_token

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(menu_router,
                       profile_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())