from pathlib import Path

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from classes.scenes.menu_scene import menu
from configs.logger import logger
from classes.manager import state_manager
from keyboards.menu_keyboard import create_menu_keyboard
from states.profile import ProfileStates
from states.registration import RegistrationStates


class TransitionManager:
    """
    Класс отвечает за переходы между сценариями


    Хэндлеры срабатывают в момент нажатия кнопки "Назад"
    в одном из состояний и определяют логику перехода
    в предыдущее состояние
    """
    def __init__(self):
        self.prev_state_command = {
            ProfileStates.unauthenticated: self.handle_start_profile,
            ProfileStates.authenticated: self.handle_start_profile,
            RegistrationStates.sending_number: self.handle_start_registration,
            RegistrationStates.sending_email: self.handle_asking_email
        }
        self.next_state_command = {
            RegistrationStates.sending_email: self.handle_asking_username,
        }


    async def remove_inline_keyboard_last_msg(self, message: Message):
        """
        Бот перед отправкой нового сообщения очищает последнее отправленное
        от inline-кнопок
        """
        # Поверяем есть ли у последнего сообщения кнопки, если да, то удаляем их
        chat_id = message.chat.id
        user_last_bot_msg = state_manager.users_last_bot_msg.get(chat_id, None)
        try:
            if user_last_bot_msg.reply_markup is not None:
                await (state_manager.users_last_bot_msg[chat_id].
                       edit_reply_markup(reply_markup=None))
        except TelegramBadRequest:
            return


    async def return_menu_scene(self, message: Message):
        """
        Возращает из любого этапа сценария в главное меню
        по reply-кнопке

        Args:
            - message(Message): объект сообщения от бота
        """
        chat_id = message.chat.id

        await self.remove_inline_keyboard_last_msg(message)

        # Отправляем временное  сообщение в чат, чтобы удалить reply-кнопку
        temp_msg = await message.answer(
            text='Возвращаемся в главное меню',
            reply_markup=ReplyKeyboardRemove()
        )
        # Удаляем временное сообщение
        await temp_msg.delete()

        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer_photo(
                caption=menu.text,
                photo=FSInputFile(str(
                    (Path(__file__).parent / '..' / '..' /
                     'img' / 'menu.jpg').resolve())),
                reply_markup=await create_menu_keyboard()
            )


    async def add_and_set_state(self, state: FSMContext, new_state: State):
        """
        Добавляет новое состояние в стек состояний, сохраняя текущее
        в истории

        Args:
            - state(FSMContext): контекст состояния
            - new_state(State): новое состояние,
                                которое необходимо установить
        """
        # Получаем текущее состояние
        history = await state.get_data()
        # Получаем стек состояний
        stack = history.get("state_stack", [])
        current_state = await state.get_state()
        if current_state:
            # Добавляем текущее состояние в стек
            stack.append(current_state)
        logger.info(f'Текущий список состояний {stack}')
        # Обновляем стек
        await state.update_data(state_stack=stack)
        # Устанавливаем состояние
        await state.set_state(new_state)


    async def handle_start_profile(self, message: Message):
        """
        Обработчик для перехода в состояния ProfileStates.authenticated
        и ProfileStates.unauthenticated
        Отображает профиль в зависимости от значения is_auth

        Args:
           - message(Message): объект сообщения от бота
        """
        from classes.scenes.profile_scene import profile

        await profile.start_scene(message)


    async def handle_start_registration(self, message: Message):
        """
        Обработчик для перехода в состояние
        RegistrationStates.sending_number
        Запускает сценарий регистрации - запрашивает номер телефона

        Args:
           - message(Message): объект сообщения от бота
        """
        from classes.scenes.registration_scene import registration_scene

        await registration_scene.start_scene(message)


    async def handle_asking_email(self, message: Message):
        """
        Обработчик для перехода в состояние
        RegistrationStates.sending_email
        Удаляет inline-клавиатуру у последнего сообщения
        и запрашивает у пользователя email

        Args:
           - message(Message): объект сообщения от бота
        """
        from classes.scenes.registration_scene import registration_scene

        await self.remove_inline_keyboard_last_msg(message)
        await registration_scene.ask_email(message)


    async def handle_asking_username(self, message: Message):
        """
        Обработчик для пропуска состояния RegistrationStates.sending_email
        перехода в состояние RegistrationStates.getting_username
        Запрашивает имя пользователя и получает его

        Args:
           - message(Message): объект сообщения от бота
        """
        from classes.scenes.registration_scene import registration_scene

        await self.remove_inline_keyboard_last_msg(message)
        await registration_scene.ask_username(message)


transition = TransitionManager()