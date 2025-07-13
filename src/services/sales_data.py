import requests
from bs4 import BeautifulSoup

class SalesData:
    @staticmethod
    async def get_data() -> list[dict]:
        """
        Асинхронно получает список акций
        со страницы https://sto-orbita.ru/spec/

        Выполняет HTTP-запрос к странице с акциями,
        парсит HTML и извлекает данные о каждой акции

        Returns:
            - sales(list[dict]): список словарей с информацией об акциях.
                                 Ключи каждого словаря:
                                    - 'title'(str): заголовок акции
                                    - 'description'(str): описание акции
                                    - 'link'(str): ссылка на подробности акции
        """
        url = 'https://sto-orbita.ru/spec/'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        sales = []

        # На странице акции находятся в блоках с классом "wx_news"
        blocks = soup.find_all('div', class_='wx_news')

        for block in blocks:
            # Заголовок акции - текст ссылки <a>
            a_tag = block.find('a', class_='u-link-v5')
            title = a_tag.get_text(strip=True) if a_tag else 'Без заголовка'

            # Ссылка на акцию
            link = a_tag['href'] if a_tag and a_tag.has_attr('href') else None

            # Описание - следующий div с классом "g-color-white-opacity-0_8"
            desc_div = block.find('div', class_='g-color-white-opacity-0_8')
            desc = desc_div.get_text(strip=True) if desc_div else ''
            sales.append({
                'title': title,
                'description': desc,
                'link': link
            })

        return sales