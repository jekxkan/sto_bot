from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.main_keyboard import create_step_back_button

async def create_change_email_button() -> InlineKeyboardButton:
    """
    Создает inline-кнопку для редактирования email

    Returns:
        - InlineKeyboardButton: объект inline-кнопки
    """
    return InlineKeyboardButton(text="Изменить адрес электронной почты",
                              callback_data="change_email")


async def create_profile_keyboard() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для сценария профиля,
    когда пользователь аутентифицирован

    Returns:
        - InlineKeyboardMarkup: inline-клавиатура

    """
    buttons = [
        [await create_change_email_button()],
        [await create_step_back_button()]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def create_unauth_profile_keyboard() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для сценария профиля,
    когда пользователь не аутентифицирован

    Returns:
        - InlineKeyboardMarkup: inline-клавиатура
    """
    buttons = [
        [InlineKeyboardButton(text="Зарегистрироваться",
                              callback_data="registrate")],
        [await create_step_back_button()]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def create_change_email_keyboard() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатура для сценария изменения email пользователя

    Returns:
        - InlineKeyboardMarkup: inline-клавиатура
    """
    buttons = [
        [await create_step_back_button()],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)