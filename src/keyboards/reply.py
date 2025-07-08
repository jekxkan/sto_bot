from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ReplyKeyboard:
    """
    Класс для создания reply-кнопок
    """
    def create_back_to_menu_button(self) -> ReplyKeyboardMarkup:
        """
        Создает reply-кнопку для возрата в меню

        Returns:
            - ReplyKeyboardMarkup: клавиатура с кнопкой "Главное меню"
        """
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Главное меню')]],
                                   resize_keyboard=True)