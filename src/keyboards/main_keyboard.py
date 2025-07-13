from typing import List

from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


class MainKeyboard:
    def __init__(self):
        self.back_button = InlineKeyboardButton(
            text="Назад", callback_data="step_back"
        )

    def create_back_to_menu_keyboard(self) -> ReplyKeyboardMarkup:
        """
        Создает reply-клавиатуру для возрата в меню

        Returns:
            - ReplyKeyboardMarkup: клавиатура с кнопкой "Главное меню"
        """
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Главное меню')]],
                                   resize_keyboard=True)


    def create_scrolling_buttons(self, page_num: int, page_quanity: int) \
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