from configs.logger import logger


class User:
    def __init__(self):
        self.data = {}

    async def write_user_data(self) -> str:
        """
        Возращает отформатированную строку с данными пользователя

        Returns:
            - str: текстовое представление данных пользователя
        """
        email = self.data.get('email', None)
        if not email:
            return (f'Ваши данные:\nИмя: {self.data["username"]}\n'
             f'Тел.: {self.data["number"]}\n')

        return (f'Ваши данные:\nИмя: {self.data["username"]}\n'
                f'Тел.: {self.data["number"]}\n'
                f'Электронная почта: {self.data["email"]}')


    async def change_email(self, new_email: str):
        """
        Обновляет поле email в атрибуте self.dara

        Args:
            - new_email(str): новый email пользователя
        """
        self.data["email"] = new_email
        logger.info(f'Новые данные пользователя: {self.data}')