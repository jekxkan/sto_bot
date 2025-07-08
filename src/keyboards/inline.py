from typing import List

from aiogram.types import InlineKeyboardButton


class InlineKeyboard:
    """
    Класс для создания inline-кнопок
    """
    def __init__(self):
        self.back_button = InlineKeyboardButton(
            text="Назад", callback_data="step_back"
        )


    def create_menu_buttons(self) -> List[List[InlineKeyboardButton]]:
        """
        Создает inline-кнопки меню

        Returns:
            - List[List[InlineKeyboardButton]]: список из объектов inline-кнопок
        """

        return [
            [InlineKeyboardButton(text="Записаться на ТО", callback_data="sing_up")],
            [InlineKeyboardButton(text="Личный кабинет", callback_data="profile")],
            [InlineKeyboardButton(text="Рассчитать стоимость ремонта",
                                  callback_data="repair")],
            [InlineKeyboardButton(text="Наши акции", callback_data="sales")]
         ]


    def create_profile_buttons(self)-> List[List[InlineKeyboardButton]]:
        """
        Создает inline-кнопки для сценария профиля,
        когда пользователь аутентифицирован

        Returns:
            - List[List[InlineKeyboardButton]]: список из объектов inline-кнопок

        """

        return [
            [InlineKeyboardButton(text="Изменить адрес электронной почты",
                                  callback_data="change_email")],
            [self.back_button]
        ]

    def create_unauth_profile_buttons(self) -> List[List[InlineKeyboardButton]]:
        """
        Создает inline-кнопки для сценария профиля,
        когда пользователь не аутентифицирован

        Returns:
            - List[List[InlineKeyboardButton]]: список из объектов inline-кнопок
        """
        return [
            [InlineKeyboardButton(text="Зарегестрироваться",
                                  callback_data="registrate")],
            [self.back_button]
        ]

    def create_change_email_buttons(self) -> List[List[InlineKeyboardButton]]:
        """
        Создает inline-кнопки для сценария изменения email пользователя

        Returns:
            - List[List[InlineKeyboardButton]]: список из объектов inline-кнопок
        """
        return [
            [self.back_button],
        ]