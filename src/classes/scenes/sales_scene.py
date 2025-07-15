from aiogram.types import Message

from classes.manager import state_manager
from classes.scene import Scene
from classes.transition import transition
from keyboards.main_keyboard import create_back_to_menu_keyboard
from utils.sales import get_sales_data

from keyboards.sales_keyboard import create_sales_keyboard


class SalesScene(Scene):
    """
    Сценарий для отображения и навигации по акциям
    """
    def __init__(self):
        super().__init__()
        self.text = 'Актуальные акции: '
        self.sales_info = None
        self.sales_count = None


    async def start_scene(self, message: Message):
        """
        Получает данные о текущих акциях, формирует inline-клавиатуру
        для их просмотра

        Args:
            - message(Message): объект сообщения
        """
        chat_id = message.chat.id

        await transition.remove_inline_keyboard_last_msg(message)
        await message.answer(
            self.text,
            reply_markup=await create_back_to_menu_keyboard(),
        )

        self.sales_info = await get_sales_data()
        self.sales_count = len(self.sales_info)

        buttons = await create_sales_keyboard(
            page_num=1,
            page_quanity=self.sales_count)

        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer(
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


    async def get_next_sale(self, message: Message, sale_num: int):
        """
        Обновляет сообщение с информацией об акции
        и клавиатурой навигации. Записывает последнее сообщение в
        BotManager.last_msg

        Args:
            - sale_num(int): номер акции
        """
        chat_id = message.chat.id

        buttons = await create_sales_keyboard(
            page_num = sale_num,
            page_quanity = self.sales_count)

        await state_manager.users_last_bot_msg[chat_id].edit_text(
            text=await self._generate_sale_text(sale_num),
            reply_markup=buttons
        )


sales = SalesScene()