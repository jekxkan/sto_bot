import asyncio

from aiogram import Bot, Dispatcher

from configs.environment import settings
from routers.errors import error_router
from routers.main import router
from routers.menu import menu_router
from routers.profile import profile_router
from routers.registration import registration_router
from routers.sales import sales_router

API_TOKEN = settings.bot_token

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(router,
                       error_router,
                       menu_router,
                       profile_router,
                       sales_router,
                       registration_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())