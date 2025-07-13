from aiogram.types import Message

from src.keyboards.main_keyboard import MainKeyboard
from src.classes.manager import BotManager
from abc import ABC, abstractmethod

from src.classes.transition import Transition


class Scene(BotManager, ABC):
    """
    Абстрактный класс для сценариев бота
    """
    def __init__(self):
        super().__init__()
        self.picture = None
        self.text = None
        self.reply_keyboard = (
            MainKeyboard().create_back_to_menu_keyboard()
        )
        self.inline_keyboard = None
        self.transition = Transition()


    async def start_scene(self, message: Message, **kwargs):
        """
        Выполняет общие шаги для начала сценария и затем запускает
        специфичную логику

        Args:
            - message(Message): объект сообщения
            - **kwargs: дополнительные параметры
        """
        await self.transition.remove_inline_keyboard_last_msg()
        await message.answer(
            self.text,
            reply_markup=self.reply_keyboard
        )

        await self._run_certain_scene(message, **kwargs)

    @abstractmethod
    async def _run_certain_scene(self, message: Message, **kwargs):
        """
        Абстрактный метод, который должен быть реализован в дочерних классах
        для специфичной логики сценария
        """
        pass