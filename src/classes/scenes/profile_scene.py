from aiogram.types import Message

from classes.transition import transition
from keyboards.main_keyboard import create_back_to_menu_keyboard
from keyboards.profile_keyboard import (create_profile_keyboard,
                                        create_unauth_profile_keyboard,
                                        create_change_email_keyboard)
from classes.manager import state_manager
from classes.scene import Scene


class ProfileScene(Scene):
    """
    Класс для сценария перехода в личный кабинет

    При вызове любого из методов мы записываем последнее отправленное
    сообщение пользователю ботом в StateManager.users_last_msg
    по id чата для отслеживания его состояния
    """
    def __init__(self):
        super().__init__()


    async def start_scene(self, message: Message):
        """
        Запускаем сценария личныго кабинета: выводим данные
        пользователя/сообщение о необходимости регистрации
        + соответствующие inline-кнопки

        Args:
           - message(Message): объект сообщения от бота
        """

        chat_id = message.chat.id
        user = state_manager.users.get(chat_id, None)

        if user:
            profile_text = await user.write_user_data()
            self.text = profile_text
            is_auth = True
        else:
            profile_text = 'Вы еще не зарегистрированы в нашей системе'
            self.text = profile_text
            is_auth = False

        await transition.remove_inline_keyboard_last_msg(message)
        await message.answer(
            self.text,
            reply_markup=await create_back_to_menu_keyboard(),
        )

        buttons = await create_profile_keyboard() if is_auth \
            else await create_unauth_profile_keyboard()

        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer(
                'Выберите действие:',
                reply_markup=buttons
            )


    async def ask_new_email(self, message: Message):
        """
        Запрашиваем новую почту, используется в сценарии профиля при нажатии
        кнопки "Изменить адрес электронной почты"(change_email)

        Args:
            - message(Message): объект сообщения от бота
        """
        chat_id = message.chat.id
        await transition.remove_inline_keyboard_last_msg(message)

        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer(
                "Введите новый адрес электронной почты:",
                reply_markup=await create_change_email_keyboard()
            )


    async def confirm_new_email(self, message: Message,  new_email: str):
        """
        Подтверждаем редактирование email пользователем и вызываем
        у экземмпляра класса User метод обновления email.
        Используется в момент, когда состояние изменилось
        на AuthStates.change_email

        Args:
            - message(Message): объект сообщения от бота
            - new_email(str): новый email пользователя
        """
        chat_id = message.chat.id

        await transition.remove_inline_keyboard_last_msg(message)
        await (state_manager.users[chat_id].
               change_email(new_email))
        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer(
                f'Ваш электронный адрес изменен!\n\n'
                f'{await state_manager.users[chat_id].write_user_data()}',
                reply_markup=None
            )


profile = ProfileScene()