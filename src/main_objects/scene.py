import asyncio

from aiogram.types import Message, InlineKeyboardMarkup, FSInputFile, ReplyKeyboardRemove

from src.keyboards.inline import InlineKeyboard
from src.main_objects.manager import BotManager

inline_keyboard = InlineKeyboard()

class Scene(BotManager):
    """
    Базовый класс для сценариев бота
    """
    def __init__(self):
        """
        Переопределяем атрибут reply_keyboard
        """
        super().__init__()
        self.reply_keyboard = self.reply_keyboard.create_back_to_menu_button()

    async def return_menu(self, message: Message):
        """
        Возращает из любого этапа сценария в главное меню
        по reply-кнопке

        Args:
            - message(Message): объект сообщения от пользователя
        """
        await self.prepare_chat()

        # Отправляем временное  сообщение в чат, чтобы удалить reply-кнопку
        temp_msg = await message.answer(text='Возвращаемся в главное меню',
                             reply_markup=ReplyKeyboardRemove())
        # Пауза 1 секунда
        await asyncio.sleep(1)
        # Удаляем временное сообщение
        await temp_msg.delete()

        buttons = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard.create_menu_buttons()
        )
        BotManager.last_msg = await message.answer_photo(caption='Добро пожаловать',
                                   photo=FSInputFile('img/pic1.jpg'),
                                   reply_markup=buttons)