from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from configs.logger import logger
from classes.transition import transition
from states.registration import RegistrationStates

router = Router()

@router.message(F.text == "🏠 Главная")
async def on_main_menu_msg(message: Message, state: FSMContext):
    """
    Обработчик сообщения "Главное меню"
    Возвращает пользователя в главное меню и сбрасывает состояние

    Args:
       - message(Message): объект сообщения от пользователя
       - state(FSMContext): контекст состояния
    """
    logger.info('Пользователь вернулся в главное меню')
    await transition.return_menu_scene(message)
    await state.clear()


@router.callback_query(lambda x: x.data == "step_back")
async def on_step_back_callback(callback: CallbackQuery, state: FSMContext):
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

    if stack:
        # Если стек не пуст, то удаляем последнее записанное состояние,
        # обновляем стек и возращаемся в последнее записанное состояние
        prev_state = stack.pop()
        await state.update_data(state_stack=stack)
        await state.set_state(prev_state)
        logger.info(f"Возврат в предыдущее состояние: {prev_state}")

        handler = transition.prev_state_command.get(prev_state)
        if handler:
            await handler(callback.message)
        else:
            logger.warning(f"Нет обработчика для состояния {prev_state}")
            await transition.return_menu_scene(callback.message)
    else:
        # Если стек пуст, то возращаемся в гланое меню и очищаем состояние
        await state.clear()
        await transition.return_menu_scene(callback.message)
        logger.info("Стек состояний пуст, возврат в главное меню")

    await callback.answer()


@router.callback_query(lambda x: x.data == "next_step")
async def on_next_step_callback(callback: CallbackQuery, state: FSMContext):
    """
    Универсальный обработчик кнопки "Пропустить"
    Переносит пользователя из текущего состояния в следующее
    (в то, которое соответствует текущему в словаре next_state)

    Args:
        - callback(CallbackQuery): объект callback-запроса
        - state(FSMContext): контекст состояния
    """
    current_state = await state.get_state()

    next_state = {
        RegistrationStates.sending_email: RegistrationStates.sending_username
    }
    next_state = next_state.get(current_state)

    if next_state:
        await transition.add_and_set_state(state=state, new_state=next_state)
        await state.set_state(next_state)
        logger.info(f"Проскакиваем с {current_state} на {next_state}")

        handler = transition.next_state_command.get(current_state)
        if handler:
            await handler(callback.message, state)
        else:
            logger.warning(f"Нет обработчика для состояния {current_state}")
            await transition.return_menu_scene(callback.message)
    else:
        await state.clear()
        await transition.return_menu_scene(callback.message)
        logger.info("Следующего состояния нет, возврат в главное меню")

    await callback.answer()


@router.callback_query(lambda x: x.data == "sing_up" or x.data == "repair")
async def on_unrealized_callback(callback: CallbackQuery):
    """
    Обработчик-заглушка для нереализованных разделов
    """
    await callback.answer(
        text='В разработке'
    )


@router.callback_query(lambda x: x.data == 'ignore')
async def on_ignore_callback(callback: CallbackQuery):
    """
    Универсальный обработчик нефункциональной кнопки
    При нажатии ничего не происходит

    Args:
        - callback(CallbackQuery): объект callback-запроса
    """
    await callback.answer()