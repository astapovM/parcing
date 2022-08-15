import csv
import datetime
import json
import time

import requests
from bs4 import BeautifulSoup

start_time = time.time()


def get_data():
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    with open(f"labirint_{cur_time}.csv", 'w', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название",
                "Автор",
                "Издательство",
                "Прежняя цена",
                "Новая цена",
                "Скидка % ",
                "Наличие: "
            )

        )
    url = "https://www.labirint.ru/genres/2308/?display=table"
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    page_count = int(soup.find('div', class_='pagination-numbers').find_all('a')[-1].text)

    books_list = []
    for page in range(1, page_count + 1):
        # for page in range(1,2):
        url = f"https://www.labirint.ru/genres/2308/?display=table&page={page}"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        books_items = soup.find(class_='products-table__body').find_all('tr')
        for bi in books_items:
            book_data = bi.find_all('td')
            try:
                book_title = book_data[0].find('a').text.strip()
            except:
                book_title = 'Нет названия'

            try:
                book_author = book_data[1].find('a').text
            except:
                book_author = 'Нет автора'

            try:
                book_public = book_data[2].find('a').text
            except:
                book_public = "Нет издательства"

            try:
                book_old_price = int(book_data[3].find(class_='price-gray').text.strip().replace(' ', ''))
            except:
                book_old_price = "Нет старой цены"

            try:
                book_new_price = int(book_data[3].find(class_='price-val').find('span').text.strip().replace(' ', ''))
            except:
                book_new_price = "Нет новой цены"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except:
                book_sale = "Нет скидки"

            try:
                book_status = book_data[-1].text
            except:
                book_status = "Нет данных"

            # print(book_title)
            # print(book_author)
            # print(book_public)
            # print(book_old_price)
            # print(book_new_price)
            # print('Скидка',' ',book_sale,'%',sep='')
            # print("#"*15)

            books_list.append(
                {
                    "Название": book_title,
                    "Автор": book_author,
                    "Издательство": book_public,
                    "Прежняя цена": book_old_price,
                    "Новая цена": book_new_price,
                    "Скидка % ": book_sale,
                    "Наличие: ": book_status
                }
            )

            with open(f"labirint_{cur_time}.csv", 'a', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_public,
                        book_old_price,
                        book_new_price,
                        book_sale,
                        book_status
                    )

                )
        print(f'Страница {page} из {page_count} сохранена')

    with open("books_items.json", 'w', encoding='utf-8') as file:
        json.dump(books_list, file, indent=4, ensure_ascii=False)


def main():
    get_data()



if __name__ == '__main__':
    main()
