import logging
import sqlite3
from collections.abc import Sequence

from data_classes import FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork, AbstractDataclass

logger = logging.getLogger('extractor')


class SQLiteExtractor:
    """Класс для работы с чтением из SQLIte"""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def _extract(self, table: str, chunk_size: int) -> Sequence[list]:
        """Метод чтения строк из базы данных.

        Читает данные из переданной таблицы итеративно по chunk_size.
        Внутри себя реализует генератор

        Args:
            table:  Имя базы данных
            chunk_size: Размер порции данных для чтения

        Yields:
            data: Список строк из базы данных
        """
        cur = self._conn.cursor()
        cur.execute(f'SELECT * FROM {table} LIMIT {chunk_size};')
        offset = chunk_size
        data = cur.fetchall()
        while data:
            yield data
            cur.execute(f'SELECT * FROM {table} LIMIT {chunk_size} OFFSET {offset};')
            data = cur.fetchall()
            offset += chunk_size
        cur.close()

    def extract_data(self, chunk_size: int = 100) \
            -> Sequence[FilmWork | Genre | Person | GenreFilmWork | PersonFilmWork]:
        """Метод конвертации прочитанных строк из базы данных в объекты dataclass`ов"""
        for data_cls in AbstractDataclass.__subclasses__():
            try:
                for chunk in self._extract(data_cls.table_name, chunk_size):
                    yield [data_cls.from_dict(dict(obj)) for obj in chunk]
            except sqlite3.OperationalError:
                logger.error('Невозможно подключиться к базе чтения', exc_info=True)
            except sqlite3.Error:
                logger.error('Ошибка чтения данных', exc_info=True)
