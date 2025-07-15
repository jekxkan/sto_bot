from aiogram.types import InlineKeyboardMarkup

from keyboards.main_keyboard import (create_scrolling_buttons,
                                     create_step_back_button)


async def create_sales_keyboard(page_num: int, page_quanity: int) \
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
    scrolling_buttons = await create_scrolling_buttons(page_num,
                                                 page_quanity)
    buttons = [scrolling_buttons, [await create_step_back_button()]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
