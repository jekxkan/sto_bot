from aiogram.types import Message, FSInputFile

from src.keyboards.menu_keyboard import MenuKeyboard
from src.classes.manager import BotManager
from src.classes.scene import Scene


class MainMenu(Scene):
    """
    Главное меню наследует метод prepare_chat и атрибуты
    класса BotManager
    """
    def __init__(self):
        """
        Переопределяются атрибуты picture, text и inline_keyboard
        """
        super().__init__()
        self.picture = '../img/pic1.jpg'
        self.text = 'Добро пожаловать'
        self.inline_keyboard = MenuKeyboard()


    async def _run_certain_scene(self, message: Message, **kwargs):
        pass


    async def start_scene(self, message: Message, **kwargs):
        """
        Отправляет сообщение с главным меню по команде /start

        В конце записываем последнее отправленное
        сообщение пользователю ботом в BotManager.last_msg
        для отслеживания состояния чата

        Args:
            - message(Message): объект сообщения от пользователя
        """
        photo = FSInputFile(self.picture)
        BotManager.last_bot_msg = await message.answer_photo(
            photo=photo,
            caption=self.text,
            reply_markup=self.inline_keyboard.create_menu_keyboard()
        )

menu = MainMenu()