from src.configs.logger import logger


class User:
    def __init__(self, data: dict = None):
        self.data = {
            'name': 'msdsks',
            'number': '320390-',
            'email': 'dcspkc'
        }

    async def write_data(self) -> str:
        """
        Возращает данные отформатированную строку с данными пользователя

        Returns:
            - str: текстовое представление данных пользователя
        """
        return (f'Ваши данные:\nИмя: {self.data["name"]}\n'
                f'Тел.: {self.data["number"]}\n'
                f'Электронная почта: {self.data["email"]}')


    async def change_email(self, new_email: str):
        """
        Обновляет поле email в атрибуте self.dara

        Args:
            - new_email(str): новый email пользователя
        """
        self.data["email"] = new_email
        logger.info(f'Новые данные пользвоателя: {self.data}')

    async def exit(self):
        pass