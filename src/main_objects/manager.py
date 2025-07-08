from src.keyboards.inline import InlineKeyboard
from src.keyboards.reply import ReplyKeyboard
from src.main_objects.user import User


class BotManager:
    """
    Базовый класс, содержащий в себе все общие функции и атрибуты
    других сущностей проекта: бот, меню и сценарии
    """
    # Создаем переменную для того, чтобы отслеживать состояние пользователя
    last_msg = None
    # Создаем объект пользователя
    user = User()

    def __init__(self):
        self.picture = None
        self.text = None
        self.inline_keyboard = InlineKeyboard()
        self.reply_keyboard = ReplyKeyboard()

    async def prepare_chat(self):
        """
        Бот перед отправкой нового сообщения очищает последнее отправленное
        от inline-кнопок
        """
        # Поверяем есть ли у последнего сообщения кнопки, елс да, то удлаяем их
        if BotManager.last_msg.reply_markup is not None:
            await BotManager.last_msg.edit_reply_markup(reply_markup=None)