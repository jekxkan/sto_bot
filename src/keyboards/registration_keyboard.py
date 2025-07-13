from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from src.keyboards.main_keyboard import MainKeyboard


class RegistrationKeyboard(MainKeyboard):
    def create_gettting_number_keyboard(self):
        """
        Создает reply-клавиатуру для получения номера телефона

        Returns:
            - ReplyKeyboardMarkup: клавиатура с кнопкой "Поделиться телефоном"
        """
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text='Поделиться телефоном',
                                      request_contact=True
                                      )
                       ]],
            resize_keyboard=True, one_time_keyboard=True)


    def create_getting_email_keyboard(self):
        """
        Создает inline-клавиатуру для получение эл. почты

        Returns:
            - InlineKeyboardMarkup: клавиатура с кнопками "Назад" и
                                    "Пропустить"
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [self.back_button],
                [InlineKeyboardButton(text='Пропустить', callback_data='next_step')],
            ]
        )