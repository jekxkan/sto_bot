from aiogram.types import Message

from src.keyboards.sales_keyboard import SalesKeyboard
from src.classes.manager import BotManager
from src.classes.scene import Scene
from src.services.sales_data import SalesData


class SalesScene(Scene):
    """
    Сценарий для отображения и навигации по акциям
    """
    def __init__(self):
        super().__init__()
        self.text = 'Актуальные акции: '
        self.sales_info = None
        self.sales_count = None
        self.inline_keyboard = SalesKeyboard()


    async def _run_certain_scene(self, message: Message, **kwargs):
        """
        Получает данные о текущих акциях, формирует inline-клавиатуру
        для их просмотра

        Args:
            - message(Message): объект сообщения
            - **kwargs: дополнительные данные
        """
        self.sales_info = await SalesData.get_data()
        self.sales_count = len(self.sales_info)

        buttons = self.inline_keyboard.create_sales_keyboard(
            page_num=1,
            page_quanity=self.sales_count)

        BotManager.last_bot_msg = await message.answer(
            text=await self._generate_sale_text(1),
            reply_markup=buttons
        )


    async def _generate_sale_text(self, sale_num: int) -> str:
        """
        Формирует текстовое описание акции по её номеру в списке

        Args:
            - sale_num(int): номер акции

        Returns:
            - str: текст с заголовком, описанием и ссылкой
        """
        return (
            f'{self.sales_info[sale_num - 1]["title"]}\n\n'
            f'{self.sales_info[sale_num - 1]["description"]}\n\n'
            f'Подробнее: {self.sales_info[sale_num - 1]["link"]}'
        )


    async def get_next_sale(self, sale_num: int):
        """
        Обновляет сообщение с информацией об акции
        и клавиатурой навигации. Записывает последнее сообщение в
        BotManager.last_msg

        Args:
            - sale_num(int): номер акции
        """
        buttons = self.inline_keyboard.create_sales_keyboard(
            page_num = sale_num,
            page_quanity = self.sales_count)

        await BotManager.last_bot_msg.edit_text(
            text=await self._generate_sale_text(sale_num),
            reply_markup=buttons
        )


sales = SalesScene()