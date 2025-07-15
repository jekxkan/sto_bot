from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру меню

    Returns:
        - InlineKeyboardMarkup: inline-клавиатура
    """
    buttons = [
        [InlineKeyboardButton(text="🚗 Записаться на ТО", callback_data="sing_up")],
        [InlineKeyboardButton(text="👤 Личный кабинет", callback_data="profile")],
        [InlineKeyboardButton(text="⚒️ Рассчитать стоимость ремонта",
                              callback_data="repair")],
        [InlineKeyboardButton(text="🔥 Наши акции", callback_data="sales")]
     ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)