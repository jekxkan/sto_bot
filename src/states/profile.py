from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.configs.logger import logger


class ProfileStates(StatesGroup):
    authenticated = State()
    registration = State()

class AuthStates(StatesGroup):
    change_email = State()

class RegistrationStates(StatesGroup):
    username = State()
    email = State()
    number = State()

async def add_state(state: FSMContext, new_state: State):
    history = await state.get_data()
    stack = history.get("state_stack", [])
    current_state = await state.get_state()
    if current_state:
        stack.append(current_state)
    logger.info(f'Текущий список состояний {stack}')
    await state.update_data(state_stack=stack)
    await state.set_state(new_state)
