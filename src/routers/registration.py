from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from classes.transition import transition
from configs.logger import logger
from classes.scenes.registration_scene import registration_scene
from states.profile import ProfileStates
from states.registration import RegistrationStates

registration_router = Router()

@registration_router.callback_query(lambda x: x.data == "registrate",
                                    ProfileStates.unauthenticated)
async def on_registrate_callback(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик callback-запроса начала регистрации пользователя

    Срабатывает при нажатии кнопки "Зарегистрироваться"
    в состоянии ProfileStates.unauthenticated
    Запускает сценарий регистрации(запрашивает номер телеефона)
    и переводит пользователя в состояние отправки номера телефона

    Args:
        - callback(CallbackQuery): объект callback-запроса
        - state(FSMContext): состояние пользователя
    """
    logger.info('Пользователь запустил сценарий регистрации')
    await registration_scene.start_scene(callback.message)
    await transition.add_and_set_state(state,
                                       RegistrationStates.sending_number)
    logger.info('Состояние: sending_number')


@registration_router.message(F.content_type == ContentType.CONTACT,
                             RegistrationStates.sending_number)
async def on_getting_number_message(message: Message, state: FSMContext):
    """
    Обработчик получения номера телефона пользователя

    Срабатывает, когда пользователь отправляет контакт
    в состоянии RegistrationStates.sending_number
    Сохраняет номер, запрашивает email и переводит пользователя
    в состояние его отправки

    Args:
        - message(Message): сообщение пользователя с контактом
        - state(FSMContext): состояние пользователя
    """
    await registration_scene.get_number(message, state)
    await transition.add_and_set_state(state,
                                       RegistrationStates.sending_email)
    await registration_scene.ask_email(message)
    logger.info('Состояние: sending_email')


@registration_router.message(RegistrationStates.sending_email)
async def on_ask_email_message(message: Message, state: FSMContext):
    """
    Обработчик отправки email пользователем

    Срабатывает, когда пользователь отправляет email
    в состоянии RegistrationStates.sending_email
    Сохраняет email, запрашивает имя и переводит пользователя
    в состояние его отправки

    Args:
        - message(Message): сообщение пользователя с email
        - state(FSMContext): состояние пользователя
    """
    await registration_scene.get_email(message, state)
    await transition.add_and_set_state(state,
                                       RegistrationStates.sending_username)
    await registration_scene.ask_username(message)
    logger.info('Состояние: sending_username')


@registration_router.message(RegistrationStates.sending_username)
async def on_username_message(message: Message, state: FSMContext):
    """
    Обработчик отправки имени пользователем

    Срабатывает, когда пользователь отправляет имя
    в состоянии RegistrationStates.sending_username.
    Сохраняет имя пользователя и завершает регистрацию,
    очищает состояние

    Args:
        - message(Message): сообщение пользователя с именем
        - state(FSMContext): состояние пользователя
    """
    await registration_scene.get_username(message, state)
    await state.clear()
    logger.info('Состояние обнулилось')