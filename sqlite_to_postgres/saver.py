import logging
from typing import Sequence

from dataclasses import fields, astuple
from psycopg2.extensions import connection as _connection
from psycopg2 import OperationalError, Error

from data_classes import FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork

logger = logging.getLogger('saver')


class PostgresSaver:
    """Класс для работы с записью в PostgreSQL"""
    def __init__(self, conn: _connection):
        self._conn = conn

    def save_data(self, data: Sequence[FilmWork | Genre | Person | GenreFilmWork | PersonFilmWork]) -> None:
        """Метод записи строк базу данных.

        Имя базы данных берется из параметра объекта конкретного Dataclass
        Нужные колонки так же берутся из параметров объекта
        Строки для записи формируются из списка объектов.

        Args:
            data: Список объектов одного из имеющихся dataclass`ов
        """
        cur = self._conn.cursor()
        table_name = self._get_table_name_by_data(data[0])
        column_names = [field.name for field in fields(data[0])]
        col_count = ', '.join(['%s'] * len(column_names))

        data = [astuple(obj) for obj in data]
        bind_values = ','.join(cur.mogrify(f'({col_count})', row).decode('utf-8') for row in data)
        column_names = ', '.join(column_names)

        query = (
            f'INSERT INTO content.{table_name} ({column_names}) VALUES {bind_values} '
            f' ON CONFLICT (id) DO NOTHING'
        )
        try:
            cur.execute(query)
        except OperationalError:
            logger.error('Невозможно подключиться к базе записи', exc_info=True)
        except Error:
            logger.error('Ошибка записи данных', exc_info=True)
        finally:
            self._conn.commit()
            cur.close()

    @staticmethod
    def _get_table_name_by_data(obj: FilmWork | Genre | Person | GenreFilmWork | PersonFilmWork) -> str:
        """Получает имя таблицы из параметра объекта dataclass"""
        return obj.table_name
