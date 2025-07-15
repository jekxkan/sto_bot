from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.main_keyboard import create_step_back_button


async def create_gettting_number_keyboard():
    """
    Создает reply-клавиатуру для получения номера телефона

    Returns:
        - ReplyKeyboardMarkup: клавиатура с кнопкой "Поделиться телефоном"
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(
            text='📞 Поделиться номером',
            request_contact=True
        )
        ]],
        resize_keyboard=True, one_time_keyboard=True
    )


async def create_getting_email_keyboard():
    """
    Создает inline-клавиатуру для получение эл. почты

    Returns:
        - InlineKeyboardMarkup: клавиатура с кнопками "Назад" и
                                "Пропустить"
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [await create_step_back_button(),
            InlineKeyboardButton(
                text='▶️ Пропустить',
                callback_data='next_step')
            ],
        ]
    )