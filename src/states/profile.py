from aiogram.fsm.state import State, StatesGroup


class ProfileStates(StatesGroup):
    authenticated = State()
    unauthenticated = State()

class AuthStates(StatesGroup):
    change_email = State()