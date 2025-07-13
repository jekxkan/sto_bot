from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.classes.transition import transition
from src.configs.logger import logger
from src.classes.manager import BotManager
from src.classes.scenes.profile_scene import ProfileScene, profile
from src.states.profile import ProfileStates, AuthStates


profile_router = Router()

@profile_router.callback_query(lambda x: x.data == "profile")
async def on_profile_callback(callback_query: CallbackQuery, state: FSMContext):
    """
    Обработчик callback-запроса "profile"
    Достает данные пользователя, переводит в состояние
    authenticated/registration в зависимости от того аутентифицирован ли пользователь
    и запускает сценарий профиля begin_scene с соответсвующими параметрами

    А также добавляет новое состояние в список

    Args:
        - callback_query(CallbackQuery): объект callback-запроса
        - state(FSMContext): контекст состояния
    """
    logger.info('Пользователь запустил сценарий личного кабинета')
    user_data = BotManager.user.data
    profile = ProfileScene(text=await BotManager.user.write_user_data())
    if user_data:
        await transition.add_and_set_state(state, ProfileStates.authenticated)
        logger.info('Состояние: authenticated')

        await profile.start_scene(callback_query.message, is_auth=True)

    else:
        await transition.add_and_set_state(state,
                                           ProfileStates.unauthenticated)
        logger.info('Состояние: unauthenticated')

        await profile.start_scene(callback_query.message, is_auth=False)


@profile_router.callback_query(lambda x: x.data == "change_email",
                               StateFilter(ProfileStates.authenticated))
async def on_change_email_callback(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик callback-запроса "change_email" для изменения email
    Переводит пользователя в состояние AuthStates.change_email
    и запрашивает новый email

    Args:
        - callback(CallbackQuery): объект callback-запроса
        - state(FSMContext): контекст состояния
    """
    await transition.add_and_set_state(state, AuthStates.change_email)
    await profile.ask_new_email(callback.message)
    await callback.answer()
    logger.info("Состояние: change_email")


@profile_router.message(AuthStates.change_email)
async def on_change_email_msg(message: Message, state: FSMContext):
    """
    Обработчик сообщений в состоянии изменения email change_email
    Подтверждает изменение email и очищает состояние

    Args:
        - message(Message): сообщение с новым email
        - state(FSMContext): контекст состояния
    """
    new_email = message.text
    await profile.confirm_new_email(message, new_email)
    await state.clear()
    logger.info(f"Email изменён на {new_email}")
    logger.info("Состояние обнулилось")