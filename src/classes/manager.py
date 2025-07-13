from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message

from src.configs.logger import logger
from src.classes.user import User
from src.states.profile import ProfileStates, AuthStates
from src.states.registration import RegistrationStates


class BotManager:
    """
    Класс для управления сценариями
    и переходами между ними
    """
    # Создаем переменную для того, чтобы отслеживать состояние пользователя
    last_bot_msg = None
    # Создаем объект пользователя
    user = User()