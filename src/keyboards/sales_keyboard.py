from aiogram.types import InlineKeyboardMarkup

from src.keyboards.main_keyboard import MainKeyboard


class SalesKeyboard(MainKeyboard):
    def create_sales_keyboard(self, page_num: int, page_quanity: int) \
            -> InlineKeyboardMarkup:
        """
        Создает inline-клавиатуру для просмотра скидок
        Args:
             - page_num(int): номер страницы
             - page_quanity(int): количество страниц
        Returns:
            - InlineKeyboardMarkup: inline-клавиатура для сценария
                                    просмотра скидок
        """
        scrolling_buttons = self.create_scrolling_buttons(page_num,
                                                          page_quanity)
        buttons = [scrolling_buttons, [self.back_button]]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
