# Подключение библиотек
import requests
from bs4 import BeautifulSoup as bs
def parse():
    # URL страницы каталога с результатами поиска по слову "Python"(с которого будет парситься информация)
    url = "https://www.chitai-gorod.ru/search?phrase=Python"
    # Заголовки запроса, чтобы сервер считал запрос от реального браузера
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    # Отправка GET-запроса к сайту с указанными заголовками
    page = requests.get(url, headers=headers)
    # Создание объекта BeautifulSoup для разбора HTML-кода данной страницы
    soup = bs(page.text, "html.parser")
    # Поиск необходимых элементов
    product_cards = soup.find_all("article", class_=lambda x: x and "product-card" in x)
    # encoding="utf-8" нужна для корректной работы с кириллицей(знак рубля)
    with open("books.csv", "w", encoding="utf-8") as f:
        # Записывание заголовки столбцов
        f.write("Название;Автор;Цена\n")  # Разделитель — точка с запятой
        # Перебор каждой карточки товара из найденных
        for card in product_cards:
            # Поиск ссылки (<a>) с классом "product-card__title"
            name = card.find("a", class_="product-card__title").text.strip()
            # Поиск элемента <span> с классом "product-card__subtitle"
            author = card.find("span", class_="product-card__subtitle").text.strip()
            # Поиск элемента с классом, который содержит "price--reverse"
            # lambda проверяет наличие подстроки в имени класса
            price_raw = card.find("span", class_=lambda x: x and "price--reverse" in x).text.strip()
            # Запись строки в файл
            f.write(f"{name};{author};{price_raw}\n")
if __name__ == "__main__":
    parse()  # Вызов функции парсинга