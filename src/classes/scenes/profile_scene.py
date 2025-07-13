from aiogram.types import Message

from src.keyboards.profile_keyboard import ProfileKeyboard
from src.classes.manager import BotManager
from src.classes.scene import Scene


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
        self.inline_keyboard = ProfileKeyboard()


    async def _run_certain_scene(self, message: Message, **kwargs):
        """
        Проверяет парамент is_auth и в зависимости
        от его значения добавляет ту или иную клавиатуруу

        Args:
            - message(Message): объект сообщения
            - **kwargs: дополнительные параметры
        """
        is_auth = kwargs.get('is_auth', False)
        buttons = self.inline_keyboard.create_profile_keyboard() if is_auth \
            else self.inline_keyboard.create_unauth_profile_keyboard()

        BotManager.last_bot_msg = await message.answer(
            'Выберите действие:',
            reply_markup=buttons
        )


    async def ask_new_email(self, message: Message):
        """
        Запрашиваем новую почту, используется в сценарии профиля при нажатии
        кнопки "Изменить адрес электронной почты"(change_email)

        Args:
            - callback(CallbackQuery): информация о нажатой кнопке
        """
        await self.transition.remove_inline_keyboard_last_msg()

        BotManager.last_bot_msg = await message.answer(
            "Введите новый адрес электронной почты:",
            reply_markup=self.inline_keyboard.create_change_email_keyboard()
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
        await self.transition.remove_inline_keyboard_last_msg()
        await BotManager.user.change_email(new_email)
        BotManager.last_bot_msg = await message.answer(
            f'Ваш электронный адрес изменен!\n\n'
            f'{await BotManager.user.write_user_data()}',
            reply_markup=None)


profile = ProfileScene()