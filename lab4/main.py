import pymongo
from pprint import pprint

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['hh_vacancies']
collection = db['jobs']


scraped_data = [
    {
        'name': 'Python Developer',
        'link': 'https://hh.ru/vacancy/111111',  # Уникальный идентификатор
        'salary_min': 80000,
        'salary_max': 120000,
        'currency': 'rub'
    },
    {
        'name': 'Data Scientist',
        'link': 'https://hh.ru/vacancy/222222',
        'salary_min': 150000,
        'salary_max': 250000,
        'currency': 'rub'
    },
    {
        'name': 'Junior Python',
        'link': 'https://hh.ru/vacancy/333333',
        'salary_min': 40000,
        'salary_max': 60000,
        'currency': 'rub'
    },
    {
        'name': 'Python Developer',
        'link': 'https://hh.ru/vacancy/111111',
        'salary_min': 80000,
        'salary_max': 120000,
        'currency': 'rub'
    }
]


def insert_unique_jobs(jobs_list):
    """
    Добавляет вакансии в базу, если их там еще нет.
    Проверка уникальности идет по полю 'link' (ссылка на вакансию).
    """
    added_count = 0
    for job in jobs_list:
        exists = collection.count_documents({'link': job['link']})

        if exists == 0:
            collection.insert_one(job)
            added_count += 1
        else:
            pass

    print(f"--- Процесс завершен. Добавлено новых документов: {added_count} ---")


def find_jobs_by_salary(amount):
    """
    Ищет вакансии, где salary_min > amount ИЛИ salary_max > amount.
    """
    print(f"\nРезультаты поиска (зарплата > {amount}):")

    query = {
        '$or': [
            {'salary_min': {'$gt': amount}},
            {'salary_max': {'$gt': amount}}
        ]
    }

    # Выполняем поиск
    result = collection.find(query)

    # Выводим результаты
    found = False
    for doc in result:
        found = True
        pprint(doc)

    if not found:
        print("Вакансий с такой зарплатой не найдено.")


if __name__ == '__main__':
    collection.delete_many({})

    print("Первая попытка добавления:")
    insert_unique_jobs(scraped_data)

    print("\nВторая попытка добавления (тех же данных):")
    insert_unique_jobs(scraped_data)

    try:
        user_salary = int(input("\nВведите желаемую зарплату для поиска: "))
        find_jobs_by_salary(user_salary)
    except ValueError:
        print("Пожалуйста, введите число.")