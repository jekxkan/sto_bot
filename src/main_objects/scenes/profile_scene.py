from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from src.keyboards.inline import InlineKeyboard
from src.main_objects.manager import BotManager
from src.main_objects.scene import Scene

inline_keyboard = InlineKeyboard()

class ProfileScene(Scene):
    """
    Класс для сценария перехода в личный кабинет

    При вызове любого из методов мы записываем последнее отправленное
    сообщение пользователю ботом в BotManager.last_msg
    для отслеживания состояния чата
    """
    def __init__(self, text: str = None):
        super().__init__()
        self.text = text

    async def begin_scene(self, message: Message, is_auth: bool):
        """
        Запускаем первый этап сценария личныго кабинета: выводим данные
        пользователя/сообщение о необходимости регистрации + соответствующие
        inline-кнопки

        Args:
            - message(Message): объект сообщения от пользователя
            - auth(bool): аутентифицирован ли пользователь
        """
        await self.prepare_chat()

        await message.answer(self.text, reply_markup=self.reply_keyboard)

        buttons = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard.create_profile_buttons()
            if is_auth
            else inline_keyboard.create_unauth_profile_buttons()
        )

        BotManager.last_msg = await message.answer(
            'Выберите действие:',
            reply_markup=buttons
        )


    async def ask_new_email(self, callback: CallbackQuery):
        """
        Запрашиваем новую почту, используется в сценарии профиля при нажатии
        кнопки "Изменить адрес электронной почты"(change_email)

        Args:
            - callback(CallbackQuery): информация о нажатой кнопке
        """
        await self.prepare_chat()
        buttons = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard.create_change_email_buttons()
        )
        BotManager.last_msg = await callback.message.answer(
            "Введите новый адрес электронной почты:",
            reply_markup=buttons
        )


    async def confirm_new_email(self, message: Message,  new_email: str):
        """
        Подтверждаем редактирование email пользователем и вызываем
        у экземмпляра класса User метод обновления email.
        Используется в момент, когда состояние изменилось
        на AuthStates.change_email

        Args:
            - message(Message): объект сообщения от пользователя
            - new_email(str): новый email пользователя
        """
        await self.prepare_chat()
        await BotManager.user.change_email(new_email)
        BotManager.last_msg = await message.answer(
            f'Ваш электронный адрес изменен!\n\n'
            f'{await BotManager.user.write_data()}',
            reply_markup=None)

    async def get_username(self, message: Message):
        pass

    async def get_user_email(self, message: Message):
        pass

    async def get_user_number(self, message: Message):
        pass