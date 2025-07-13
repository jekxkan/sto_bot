from aiogram import Router

from aiogram.filters import CommandStart
from aiogram.types import Message

from src.configs.logger import logger
from src.classes.scenes.menu_scene import menu

menu_router = Router()

@menu_router.message(CommandStart())
async def on_start_msg(message: Message):
    """
    Обработчик команды /start
    Отправляет в чат главное меню

    Args:
        - message(Message): объект сообщения от пользователя
    """
    logger.info('Запуск меню')
    await menu.start_scene(message)