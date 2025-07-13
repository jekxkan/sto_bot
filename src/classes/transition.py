import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from src.configs.logger import logger
from src.keyboards.menu_keyboard import MenuKeyboard
from src.classes.manager import BotManager
from src.states.profile import ProfileStates
from src.states.registration import RegistrationStates


class Transition(BotManager):
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


    async def remove_inline_keyboard_last_msg(self):
        """
        Бот перед отправкой нового сообщения очищает последнее отправленное
        от inline-кнопок
        """
        # Поверяем есть ли у последнего сообщения кнопки, елс да, то удлаяем их
        if BotManager.last_bot_msg.reply_markup is not None:
            await BotManager.last_bot_msg.edit_reply_markup(reply_markup=None)


    async def return_menu_scene(self, message: Message):
        """
        Возращает из любого этапа сценария в главное меню
        по reply-кнопке

        Args:
            - message(Message): объект сообщения от пользователя
        """
        await self.remove_inline_keyboard_last_msg()

        # Отправляем временное  сообщение в чат, чтобы удалить reply-кнопку
        temp_msg = await message.answer(text='Возвращаемся в главное меню',
                             reply_markup=ReplyKeyboardRemove())
        # Пауза 1 секунда
        await asyncio.sleep(1)
        # Удаляем временное сообщение
        await temp_msg.delete()

        BotManager.last_bot_msg = await message.answer_photo(
            caption='Добро пожаловать',
            photo=FSInputFile('../img/pic1.jpg'),
            reply_markup=MenuKeyboard().create_menu_keyboard()
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
           - message(Message): объект сообщения
        """
        from src.classes.scenes.profile_scene import ProfileScene

        profile_text = await BotManager.user.write_user_data()
        profile = ProfileScene(text=profile_text)
        user_data = BotManager.user.data
        if user_data:
            is_auth = True
        else:
            is_auth = False
        await profile.start_scene(message, is_auth=is_auth)


    async def handle_start_registration(self, message: Message):
        """
        Обработчик для перехода в состояние
        RegistrationStates.sending_number
        Запускает сценарий регистрации - запрашивает номер телефона

        Args:
           - message(Message): объект сообщения
        """
        from src.classes.scenes.registration_scene import registration_scene

        await registration_scene.start_scene(message)


    async def handle_asking_email(self, message: Message):
        """
        Обработчик для перехода в состояние
        RegistrationStates.sending_email
        Удаляет inline-клавиатуру у последнего сообщения
        и запрашивает у пользователя email

        Args:
           - message(Message): объект сообщения
        """
        from src.classes.scenes.registration_scene import registration_scene

        await self.remove_inline_keyboard_last_msg()
        await registration_scene.ask_email(message)


    async def handle_asking_username(self, message: Message, state: FSMContext):
        """
        Обработчик для пропуска состояния RegistrationStates.sending_email
        перехода в состояние RegistrationStates.getting_username
        Запрашивает имя пользователя и получает его

        Args:
           - message(Message): объект сообщения
        """
        from src.classes.scenes.registration_scene import registration_scene

        await self.remove_inline_keyboard_last_msg()
        await registration_scene.ask_username(message)


transition = Transition()