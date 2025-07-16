from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup

from classes.transition import transition
from classes.user import User
from keyboards.main_keyboard import (create_step_back_button,
                                     create_back_to_menu_keyboard)
from keyboards.registration_keyboard import (create_getting_email_keyboard,
                                             create_gettting_number_keyboard)
from classes.manager import state_manager
from classes.scene import Scene


class RegistrationScene(Scene):
    def __init__(self):
        super().__init__()
        self.text = 'Поделитесь Вашим телефонным номером:'


    async def start_scene(self, message: Message):
        """
        Запускает сценарий регистрации - запрашивает номер телефона

        Args:
            - message(Message): объект сообщения от бота
        """
        chat_id = message.chat.id

        await transition.remove_inline_keyboard_last_msg(message)
        await message.answer(
            self.text,
            reply_markup=await create_gettting_number_keyboard()
        )

        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer(
                text='Чтобы поделиться, нажмите на '
                     'кнопку "Поделиться номером" внизу',
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[await create_step_back_button()]]
                )
            )


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
        await transition.remove_inline_keyboard_last_msg(message)

        number = message.contact.phone_number
        await self.check_if_num_exists_in_1c(number)

        data = await state.get_data()
        registration_data = data.get('registration_data', {})
        registration_data['number'] = number
        await state.update_data(registration_data=registration_data)

        await message.answer(
            text=f'Ваш номер: {number}',
            reply_markup=await create_back_to_menu_keyboard()
        )


    async def ask_email(self, message: Message):
        """
        Запрашивает у пользователя адрес эл. почты

        Args:
            - message(Message): объект сообщение от бота
        """
        chat_id = message.chat.id

        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer(
                text='Введите адрес электронной почты:',
                reply_markup=await create_getting_email_keyboard()
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
        await transition.remove_inline_keyboard_last_msg(message)

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
            - message(Message): объект сообщения от бота
        """
        chat_id = message.chat.id

        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer(
                text='Укажите как к Вам обращаться: ',
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[await create_step_back_button()]]
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
        chat_id = message.chat.id

        await transition.remove_inline_keyboard_last_msg(message)

        username = message.text
        data = await state.get_data()
        registration_data = data.get('registration_data', {})
        registration_data['username'] = username
        await state.update_data(registration_data=registration_data)

        email = registration_data.get('email', None)

        state_manager.users[chat_id] = User()
        state_manager.users[chat_id].data = {
            'username': username,
            'email': email,
            'number': registration_data['number'],
        }

        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer(
                text=f'Спасибо, что зарегистрировались!\n\n'
                     f'{await state_manager.users[chat_id].write_user_data()}'
            )

registration_scene = RegistrationScene()