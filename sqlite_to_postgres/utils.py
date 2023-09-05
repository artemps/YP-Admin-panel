import psycopg2
import sqlite3
from contextlib import contextmanager
from psycopg2.extras import DictCursor


@contextmanager
def sqlite_conn_context(db_path: str):
    """Контекстный менеджер для управлени соединением с SQLite"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@contextmanager
def postgresql_conn_context(dsl):
    """Контекстный менеджер для управлени соединением с PostgreSQL"""
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield conn
    conn.close()

