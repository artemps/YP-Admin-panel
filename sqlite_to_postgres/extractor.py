import sqlite3
from collections.abc import Sequence

from data_classes import FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork, AbstractDataclass


class SQLiteExtractor:
    """Класс для работы с чтением из SQLIte"""
    def __init__(self, conn: sqlite3.Connection):
        self._cursor = conn.cursor()

    def _extract(self, table: str, chunk_size: int) -> Sequence[list]:
        """Метод чтения строк из базы данных.

        Читает данные из переданной таблицы итеративно по chunk_size.
        Внутри себя реализует генератор

        Args:
            table:  Имя базы данных
            chunk_size: Размер порции данных для чтения

        Returns:
            data: Список строк из базы данных
        """
        self._cursor.execute(f"SELECT * FROM {table} LIMIT {chunk_size};")
        offset = chunk_size
        data = self._cursor.fetchall()
        while data:
            yield data
            self._cursor.execute(f"SELECT * FROM {table} LIMIT {chunk_size} OFFSET {offset};")
            data = self._cursor.fetchall()
            offset += chunk_size

    def extract_data(self, chunk_size: int = 100) \
            -> Sequence[FilmWork | Genre | Person | GenreFilmWork | PersonFilmWork]:
        """Метод конвертации прочитанных строк из базы данных в объекты dataclass`ов"""
        for data_cls in AbstractDataclass.__subclasses__():
            try:
                for chunk in self._extract(data_cls.table_name, chunk_size):
                    yield [data_cls.from_dict(dict(obj)) for obj in chunk]
            except sqlite3.OperationalError as e:
                print(f'Невозможно подключиться к базе чтения: {e}')
            except sqlite3.Error as e:
                print(f'Ошибка чтения данных: {e}')
