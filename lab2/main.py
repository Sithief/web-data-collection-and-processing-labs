import json

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def parse_vacancies_to_df(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    data_block = soup.find('template', id='HH-Lux-InitialState')
    json_data_str = data_block.text.strip()
    json_data = json.loads(json_data_str)
    vacancies = json_data['vacancySearchResult']['vacancies']
    data = []

    for vacancy in vacancies:
        row = {
            'job_title': vacancy.get('name'),
            'company_name': vacancy.get('company', []).get('name'),
            'salary_from': vacancy.get('compensation', []).get('from'),
            'salary_to': vacancy.get('compensation', []).get('to'),
            'currencyCode': vacancy.get('compensation', []).get('currencyCode'),
            'area': vacancy.get('area', []).get('name'),
            'link': vacancy.get('links', []).get('desktop'),
            'source': 'hh.ru',
        }
        data.append(row)

    return data


def get_hh_vacancies(keyword, pages_count):
    # Обязательно притворяемся браузером
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    data = []

    for page in range(pages_count):
        print(f"Парсинг страницы {page + 1}...")
        url = 'https://hh.ru/search/vacancy'
        params = {
            'text': keyword,
            'page': page,
            'per_page': 20,
            'area': 113,
            'label': 'with_salary'
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка доступа: {e}")
            break


        new_data = parse_vacancies_to_df(response.text)
        print(f"Найдено {len(new_data)} вакансий\n\n")
        data += new_data

        time.sleep(1)  # Чтобы не получить ошибку TooManyRequests

    return data


# --- ЗАПУСК ---
if __name__ == "__main__":
    # search_text = input("Введите должность для поиска (например, Python): ")
    # try:
    #     pages = int(input("Сколько страниц искать: "))
    # except ValueError:
    #     pages = 1
    search_text = "python"
    pages = 2

    vacancies = get_hh_vacancies(search_text, pages)

    if vacancies:
        df = pd.DataFrame(vacancies)

        # Вывод первых строк
        print(df.head())

        # Сохранение
        df.to_csv('vacancies.csv', index=False, encoding='utf-8')
        df.to_json('vacancies.json', orient='records', force_ascii=False, indent=4)
        print("\nДанные сохранены в vacancies.csv и vacancies.json")
    else:
        print("Не удалось собрать данные.")