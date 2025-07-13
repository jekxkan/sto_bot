from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove

from src.keyboards.main_keyboard import MainKeyboard
from src.keyboards.registration_keyboard import RegistrationKeyboard
from src.classes.manager import BotManager
from src.classes.scene import Scene


class RegistrationScene(Scene):
    def __init__(self):
        super().__init__()
        self.text = 'Поделитесь Вашим телефонным номером:'
        self.inline_keyboard = {
            'main': MainKeyboard(),
            'registration': RegistrationKeyboard()
        }
        self.reply_keyboard = {
            'main_menu': self.reply_keyboard,
            'getting_number': RegistrationKeyboard().
                              create_gettting_number_keyboard()
        }


    async def _run_certain_scene(self, message: Message, **kwargs):
        """
        Добавляет сообщение с кнопкой "Назад"

        Args:
            - message(Message): объект сообщение
            - **kwargs: дополнительные параметры
        """
        BotManager.last_bot_msg = await message.answer(
            text='Чтобы поделиться, нажмите на кнопку "Поделиться номером" внизу',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[self.inline_keyboard['main'].back_button]]
            )
        )


    async def start_scene(self, message: Message, **kwargs):
        """
        Запускает сценарий регистрации - запрашивает номер телефона

        Args:
            - message(Message): объект сообщения
            - **kwargs: дополнительные параметры
        """
        await self.transition.remove_inline_keyboard_last_msg()
        await message.answer(
            self.text,
            reply_markup=self.reply_keyboard['getting_number']
        )

        await self._run_certain_scene(message, **kwargs)


    async def check_if_num_exists_in_1c(self, number: str):
        pass


    async def get_number(self, message: Message, state: FSMContext):
        """
        Обрабатывает получение номера телефона от пользователя,
        сохраняет его во временные данные FSMContext, обновляет
        данные пользователя и отправляет пользователю
        сообщение с его номером

        Args:
            - message(Message): сообщение пользователя с контактами
            - state(FSMContext): контекст состояния
        """
        await self.transition.remove_inline_keyboard_last_msg()

        number = message.contact.phone_number
        await self.check_if_num_exists_in_1c(number)

        data = await state.get_data()
        registration_data = data.get('registration_data', {})
        registration_data['number'] = number
        await state.update_data(registration_data=registration_data)

        await message.answer(
            text=f'Ваш номер: {number}',
            reply_markup=self.reply_keyboard['main_menu']
        )


    async def ask_email(self, message: Message):
        """
        Запрашивает у пользователя адрес эл. почты

        Args:
            - message(Message): объект сообщение
        """
        BotManager.last_bot_msg = await message.answer(
            text='Введите адрес электронной почты:',
            reply_markup=self.inline_keyboard['registration'].
                         create_getting_email_keyboard()
        )


    async def get_email(self, message: Message, state: FSMContext):
        """
        Обрабатывает получение email от пользователя,
        сохраняет его во временные данные FSMContext
        и обновляет данные пользователя

        Args:
            - message(Message): сообщение пользователя с email
            - state(FSMContext): контекст состояния FSM
        """
        await self.transition.remove_inline_keyboard_last_msg()

        email = message.text
        data = await state.get_data()
        registration_data = data.get('registration_data', {})
        registration_data['email'] = email
        await state.update_data(registration_data=registration_data)

        await message.answer(
            text=f'Ваш email: {email}'
        )


    async def ask_username(self, message: Message):
        """
        Запрашивает у пользователя имя

        Args:
            - message(Message): объект сообщения
        """
        BotManager.last_bot_msg = await message.answer(
            text='Укажите как к Вам обращаться: ',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[self.inline_keyboard['main'].back_button]]
            )
        )


    async def get_username(self, message: Message, state: FSMContext):
        """
        Обрабатывает получение имени пользователя,
        сохраняет его во временные данные FSMContext
        и обновляет данные пользователя

        Args:
            - message(Message): сообщение пользователя с именем
            - state(FSMContext): контекст состояния
        """
        await self.transition.remove_inline_keyboard_last_msg()

        username = message.text
        data = await state.get_data()
        registration_data = data.get('registration_data', {})
        registration_data['username'] = username
        await state.update_data(registration_data=registration_data)
        BotManager.user.data.update(registration_data)

        BotManager.last_bot_msg = await message.answer(
            text=f'Спасибо, что зарегистрировались!\n\n'
                 f'{await BotManager.user.write_user_data()}'
        )

registration_scene = RegistrationScene()