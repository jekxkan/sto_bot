from aiogram.types import Message, FSInputFile

from keyboards.menu_keyboard import create_menu_keyboard
from classes.manager import state_manager
from classes.scene import Scene


class MainMenu(Scene):
    """
    Главное меню наследует метод prepare_chat и атрибуты
    класса BotManager
    """
    def __init__(self):
        """
        Переопределяются атрибуты picture, text и inline_keyboard
        """
        super().__init__()
        self.picture = '../img/menu.jpg'
        self.text = ('Запишитесь на СТО Орбита уже\nсегодня и получите '
                     'качетсвенное\nобслуживание вашего авто!\n'
                     'Просто выберите желаемую дату\nи время визита.\n\n'
                     'Режим работы:\n'
                     'Ежедневно с 9:00 до 21:00\n\n'
                     'Телефоны:\n'
                     '8 (812) 454-79-79\n'
                     ' • Институтский переулок д.1\n'
                     ' • Суздальский проспект д.32\n  корп.2\n'
                     ' • ул.Руставели д.59 Е\n\n'
                     '8 (812) 454-60-60\n'
                     ' • Кожевенная линия д.29 корп.13\n'
                     ' • ул. Маршала Говорова д.29')


    async def start_scene(self, message: Message):
        """
        Отправляет сообщение с главным меню по команде /start

        В конце записываем последнее отправленное
        сообщение пользователю ботом в BotManager.last_msg
        для отслеживания состояния чата

        Args:
            - message(Message): объект сообщения от пользователя
        """
        chat_id = message.chat.id

        photo = FSInputFile(self.picture)
        state_manager.users_last_bot_msg[chat_id] = \
            await message.answer_photo(
                photo=photo,
                caption=self.text,
                reply_markup=await create_menu_keyboard()
            )

menu = MainMenu()