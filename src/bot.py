import asyncio

from aiogram import Bot, Dispatcher

from src.configs.environment import settings
from src.configs.logger import logger
from src.routers.main import router
from src.routers.menu import menu_router
from src.routers.profile import profile_router
from src.routers.registration import registration_router
from src.routers.sales import sales_router

API_TOKEN = settings.bot_token

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    try:
        dp.include_routers(router,
                           menu_router,
                           profile_router,
                           sales_router,
                           registration_router)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    asyncio.run(main())