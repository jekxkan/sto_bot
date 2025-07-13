from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    sending_username = State()
    sending_email = State()
    sending_number = State()