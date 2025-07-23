from typing import List

from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup


async def create_back_to_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает reply-клавиатуру для возрата в меню

    Returns:
        - ReplyKeyboardMarkup: клавиатура с кнопкой "Главное меню"
    """
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🏠 Главная')]],
                               resize_keyboard=True)


async def create_inline_back_to_menu_button() -> InlineKeyboardButton:
    """
    Создает inline-кнопку для возрата в меню

    Returns:
        - InlineKeyboardButton: кнопка "Главное меню"
    """
    return InlineKeyboardButton(text='🏠 Главная', callback_data='back_to_menu')


async def create_step_back_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="◀️ Назад",
        callback_data="step_back"
    )


async def create_scrolling_buttons(page_num: int, page_quanity: int) \
        -> List[InlineKeyboardButton]:
    """
    Создает inline-кнопки прокрутки данных в сообщении

    Args:
         - page_num(int): номер страницы
         - page_quanity(int): количество страниц
    Returns:
        - buttons(List[InlineKeyboardButton]): список с объектами
                                               кнопок прокрутки
    """
    buttons = []
    if page_num > 1:
        prev_page = page_num - 1
    else:
        prev_page = page_quanity
    buttons.append(InlineKeyboardButton(
        text='<',
        callback_data=f"page_{prev_page}"
    ))

    buttons.append(InlineKeyboardButton(
        text=f'{page_num}/{page_quanity}',
        callback_data='ignore'
    ))

    if page_num < page_quanity:
        next_page = page_num + 1
    else:
        next_page = 1
    buttons.append(InlineKeyboardButton(
        text='>',
        callback_data=f"page_{next_page}"
    ))
    return buttons