from lxml import html
import requests
import sqlite3


class NewsDatabase:
    def __init__(self, db_name="news.db"):
        """
        Инициализация соединения с БД.
        Если файла нет, он будет создан.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """
        Создание таблицы news, если она еще не существует.
        """
        query = """
        CREATE TABLE IF NOT EXISTS news (
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT PRIMARY KEY,
            datetime TEXT NOT NULL
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    def add_news(self, source, title, link, datetime):
        """
        Метод для добавления новой записи в БД.
        """
        query = "INSERT INTO news (source, title, link, datetime) VALUES (?, ?, ?, ?)"

        try:
            self.cursor.execute(query, (source, title, link, datetime))
            self.connection.commit()
            print(f"Добавлено: {title}")
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении в БД: {e}")

    def close(self):
        """Закрытие соединения"""
        self.connection.close()


def main():
    db = NewsDatabase("all_news.db")

    response = requests.get("https://news.mail.ru")
    tree = html.fromstring(response.content)
    common_path = tree.xpath(
        "/html/body/div[2]/div[3]/div/div/div[1]/div[3]/div/div/section/div/div[2]/div[2]/div[1]/div/div/div/div[2]",
    )

    for item in common_path:
        time_element = item.xpath("./div[1]/div/span[1]/span/time")[0]
        link_element = item.xpath("./h3/a")[0]
        db.add_news(
            source="news.mail.ru",
            title=link_element.text,
            link=link_element.attrib["href"],
            datetime=time_element.attrib["datetime"],
        )

    db.close()


main()
