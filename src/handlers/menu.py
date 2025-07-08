from aiogram import Router, types
from aiogram.filters import CommandStart

from src.configs.logger import logger
from src.main_objects.menu import MainMenu

menu_router = Router()
menu = MainMenu()

@menu_router.message(CommandStart())
async def start(message: types.Message):
    logger.info('Запуск меню')
    await menu.start(message)
