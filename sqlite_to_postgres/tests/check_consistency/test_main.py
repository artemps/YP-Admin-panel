import os
from typing import Sequence

import pytest
from sqlite3 import Cursor

from psycopg2.extensions import cursor
from dotenv import load_dotenv

from sqlite_to_postgres.utils import sqlite_conn_context, postgresql_conn_context

load_dotenv()

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT')
}
sqlite_path = os.environ.get('SQLITE_DB_PATH')


def fetch_count(cur: Cursor | cursor, query) -> int:
    """Исполнить запрос и вытащить число COUNT"""
    cur.execute(query)
    data = cur.fetchone()[0]
    return data


def fetch_data(cur: Cursor | cursor, query) -> Sequence[list]:
    """Исполнить запрос и вытащить все строки"""
    cur.execute(query)
    data = cur.fetchall()
    return data


@pytest.mark.parametrize(
    'table_name',
    ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work'],
)
def test_integrality(table_name: str):
    """Проверка целостности данных в обеих базах

    Сравнение кол-ва записей в каждой таблице между базой для чтения(SQLite)
    и базой для записи(PostgreSQL)

    Args:
        table_name: Имя таблицы
    """
    with sqlite_conn_context(sqlite_path) as sqlite_conn, postgresql_conn_context(dsl) as pg_conn:
        query = f"SELECT COUNT(*) FROM {table_name}"
        read_count = fetch_count(sqlite_conn.cursor(), query)

        query = f"SELECT COUNT(*) FROM content.{table_name}"
        write_count = fetch_count(pg_conn.cursor(), query)

        assert read_count == write_count


@pytest.mark.parametrize(
    'table_name,columns_count',
    [('film_work', 2), ('genre', 3), ('person', 2), ('genre_film_work', 3), ('person_film_work', 4)],
)
def test_content(table_name: str, columns_count: int):
    """Проверка содержимого таблиц в обеих базах

    Сравнение содержимого каждой таблицы между базой для чтения(SQLite)
    и базой для записи(PostgreSQL). Так как некоторые поля были не нужны для переноса,
    либо заполнялись новыми данными created/modified,
    то сраниваются некоторые выбранные столбцы

    Args:
        table_name: Имя таблицы
        columns_count: Кол-во столбцов от начала(id) для сверки данных
    """
    with sqlite_conn_context(sqlite_path) as sqlite_conn, postgresql_conn_context(dsl) as pg_conn:
        query = f"SELECT * FROM {table_name} ORDER BY id"
        records_from_sqlite = fetch_data(sqlite_conn.cursor(), query)
        records_from_sqlite = [list(row[:columns_count]) for row in records_from_sqlite]

        query = f"SELECT * FROM content.{table_name} ORDER BY id"
        records_from_postgres = fetch_data(pg_conn.cursor(), query)
        records_from_postgres = [row[:columns_count] for row in records_from_postgres]

        assert records_from_sqlite == records_from_postgres

