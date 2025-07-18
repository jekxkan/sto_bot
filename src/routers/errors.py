from aiogram import Router
from aiogram.types import Update, ErrorEvent

from configs.logger import logger

error_router = Router()

@error_router.errors()
async def global_error_handler(event: ErrorEvent):
    update = event.update
    error = event.exception

    if update.message:
        message = update.message
    elif update.callback_query and update.callback_query.message:
        message = update.callback_query.message

    if message:
        try:
            logger.error(error)
            await message.answer("Система в данный момент не отвечает,"
                                 "повторите попытку позже 😞")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения об ошибке: {e}")
