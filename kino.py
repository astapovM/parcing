
import json
import os
import requests
from bs4 import BeautifulSoup

film_list_2 = []
count = 0
for i in range(1, 73):
    if not os.path.exists("data"):
        os.mkdir('data')
    count+=1
    url = f"https://www.film.ru/a-z/movies/2021/ajax?page={i}&js=true"
    print(f'#{count} выполнен')
    r = requests.get(url)
    json_data = json.loads(r.text)
    html_responce = json_data[1]["data"]
    with open(f'data/index_{i}.html', 'w', encoding='utf-8') as file:
        file.write(html_responce)

    with open(f"data/index_{i}.html", encoding='utf-8') as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')
        all_films = soup.find_all('div', class_='film_list')
        for i in all_films:
            film_url = "https://www.film.ru/" + i.find(class_='film_list_link').get('href')
            film_name = i.get('title')
            film_infos = i.find_all('span')
            film_year = film_infos[2].text
            film_jenre = film_infos[3].text
            film_grade = film_infos[4].text.strip().rstrip()
            film_grade_2 = film_infos[9].text.strip()
            film_eng_name = film_infos[0].text

            film_list_2.append({
                "Фильм": film_name,
                "Ссылка": film_url,
                "Год выпуска": film_year,
                "Жанр": film_jenre})

    with open("data123.json", 'w', encoding='utf-8') as file:
        json.dump(film_list_2, file, indent=4, ensure_ascii=False)

        for i in film_list_2:
            count += 1
            print(f'#{count} успешно записан')

    #
