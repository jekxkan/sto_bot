from aiogram.fsm.state import StatesGroup, State


class SalesStates(StatesGroup):
    view_sales = State()