from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from src.configs.logger import logger
from src.main_objects.manager import BotManager
from src.main_objects.scenes.profile_scene import ProfileScene
from src.services.registration import registrate_user
from src.states.profile import ProfileStates, AuthStates, add_state

profile_router = Router()

profile = ProfileScene()
states = [ProfileStates.authenticated, ProfileStates.registration,
          AuthStates.change_email, default_state]

@profile_router.message(F.text == "Главное меню",
                        StateFilter(*states))
async def back_to_menu(message: Message, state: FSMContext):
    """
    Обработчик сообщения "Главное меню"
    Возвращает пользователя в главное меню и сбрасывает состояние

    Args:
       - message(Message): объект сообщения от пользователя
       - state(FSMContext): контекст состояния
    """
    await profile.return_menu(message)
    await state.clear()


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
    user_data = BotManager.user.data

    if user_data:
        await add_state(state, ProfileStates.authenticated)
        logger.info('Состояние: authenticated')
        profile_text = await BotManager.user.write_data()
        profile = ProfileScene(text = profile_text)

        await profile.begin_scene(callback_query.message, is_auth=True)

    else:
        await add_state(state, ProfileStates.registration)
        logger.info('Состояние: registration')

        profile = ProfileScene(text=f'Вы еще не зарегистрированы в нашей системе')
        await profile.begin_scene(callback_query.message, is_auth=False)


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
    await add_state(state, AuthStates.change_email)
    await profile.ask_new_email(callback)
    await callback.answer()
    logger.info("Состояние: change_email")


@profile_router.message(AuthStates.change_email)
async def change_email_handler(message: Message, state: FSMContext):
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
    logger.info("Состояние обнулилось")
    logger.info(f"Email изменён на {new_email}")


@profile_router.callback_query(lambda x: x.data == "step_back")
async def step_back_handler(callback: CallbackQuery, state: FSMContext):
    """
    Универсальный обработчик кнопки "Назад"
    Возвращает пользователя в предыдущее состояние из стека состояний
    Если стек пуст, то сбрасывает состояние и возвращает в главное меню

    Args:
        - callback(CallbackQuery): объект callback-запроса
        - state(FSMContext): контекст состояния
    """
    # Получаем текущий стек состояния
    data = await state.get_data()
    stack = data.get("state_stack", [])

    # Получаем актуальные данные пользователя
    profile_text = await BotManager.user.write_data()
    profile = ProfileScene(text=profile_text)

    if stack:
        # Если стек не пуст, то удаляем последнее записанное состояние,
        # обновляем стек и возращаемся в последнее записанное состояние
        prev_state = stack.pop()
        await state.update_data(state_stack=stack)
        await state.set_state(prev_state)
        logger.info(f"Возврат в предыдущее состояние: {prev_state}")

        if prev_state == ProfileStates.authenticated:
            await profile.begin_scene(callback.message, is_auth=True)
        elif prev_state == ProfileStates.registration:
            await profile.begin_scene(callback.message, is_auth=False)
        elif prev_state == AuthStates.change_email:
            await profile.ask_new_email(callback)
        else:
            await profile.return_menu(callback.message)
    else:
        # Если стек пуст, то возращаемся в гланое меню и очищаем состояние
        await state.clear()
        await profile.return_menu(callback.message)
        logger.info("Стек состояний пуст, возврат в главное меню")

    await callback.answer()


@profile_router.message(ProfileStates.registration)
async def on_registration_callback(message: Message, state: FSMContext):
    """
    Обработчик сообщений в состоянии регистрации
    Получает данные пользователя из сообщений, регистрирует пользователя

    Args:
        - message(Message): сообщение пользователя
        - state(FSMContext): контекст состояния
    """
    num = await profile.get_user_number(message)
    email = await profile.get_user_email(message)
    name = await profile.get_username(message)
    data = {
        "name": name,
        "number": num,
        "email": email,
    }
    user = await registrate_user(data)