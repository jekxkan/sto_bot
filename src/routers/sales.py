from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.classes.transition import transition
from src.configs.logger import logger
from src.classes.manager import BotManager
from src.classes.scenes.sales_scene import sales
from src.states.sales import SalesStates

sales_router = Router()

@sales_router.callback_query(lambda x: x.data == "sales")
async def on_sales_callback(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик callback-запроса перехода в раздел скидок

    Срабатывает при нажатии кнопки "Наши акции"
    Запускает сценарий раздела скидок,
    устанавливает состояние просмотра акций,

    Args:
        - callback(CallbackQuery): объект callback-запроса
        - state(FSMContext): состояние пользователя
    """
    logger.info('Пользователь запустил сценарий скидок')
    await sales.start_scene(callback.message)
    await transition.add_and_set_state(state, SalesStates.view_sales)
    await callback.answer()


@sales_router.callback_query(lambda x: x.data and x.data.startswith("page_"))
async def on_page_callback(callback: CallbackQuery):
    """
    Обработчик callback-запроса переключения страниц при просмотре акций

    Срабатывает при нажатии на inline-кнопку с callback_data вида "page_х",
    где х — номер страницы
    Загружает данные для соответствующей страницы акции

    Args:
        - callback(CallbackQuery): объект callback-запроса
    """
    page = int(callback.data.split("_")[1])
    await sales.get_next_sale(page)
    await callback.answer()
