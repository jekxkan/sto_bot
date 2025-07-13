from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.keyboards.main_keyboard import MainKeyboard


class ProfileKeyboard(MainKeyboard):
    def create_profile_keyboard(self)-> InlineKeyboardMarkup:
        """
        Создает inline-клавиатуру для сценария профиля,
        когда пользователь аутентифицирован

        Returns:
            - InlineKeyboardMarkup: inline-клавиатура

        """
        buttons = [
            [InlineKeyboardButton(text="Изменить адрес электронной почты",
                                  callback_data="change_email")],
            [self.back_button]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)


    def create_unauth_profile_keyboard(self) -> InlineKeyboardMarkup:
        """
        Создает inline-клавиатуру для сценария профиля,
        когда пользователь не аутентифицирован

        Returns:
            - InlineKeyboardMarkup: inline-клавиатура
        """
        buttons = [
            [InlineKeyboardButton(text="Зарегестрироваться",
                                  callback_data="registrate")],
            [self.back_button]
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)


    def create_change_email_keyboard(self) -> InlineKeyboardMarkup:
        """
        Создает inline-клавиатура для сценария изменения email пользователя

        Returns:
            - InlineKeyboardMarkup: inline-клавиатура
        """
        buttons = [
            [self.back_button],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)