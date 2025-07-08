from aiogram.types import Message, InlineKeyboardMarkup, FSInputFile, ReplyKeyboardRemove

from src.main_objects.manager import BotManager

class MainMenu(BotManager):
    """
    Главное меню наследует метод prepare_chat и атрибуты
    класса BotManager
    """
    def __init__(self):
        """
        Переопределяются атрибуты picture, text и inline_keyboard
        """
        super().__init__()
        self.picture = 'img/pic1.jpg'
        self.text = 'Добро пожаловать'
        self.inline_keyboard = self.inline_keyboard.create_menu_buttons()


    async def start(self, message: Message):
        """
        Отправляет сообщение с главным меню по команде /start

        В конце записываем последнее отправленное
        сообщение пользователю ботом в BotManager.last_msg
        для отслеживания состояния чата

        Args:
            - message(Message): объект сообщения от пользователя
        """
        buttons = InlineKeyboardMarkup(
            inline_keyboard=self.inline_keyboard
        )
        photo = FSInputFile(self.picture)
        BotManager.last_msg = await message.answer_photo(
            photo=photo,
            caption=self.text,
            reply_markup=buttons
        )