import logging
import os
import sqlite3

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection

from extractor import SQLiteExtractor
from saver import PostgresSaver
from utils import sqlite_conn_context, postgresql_conn_context

load_dotenv()
logging.basicConfig(level=os.environ.get('LOG_LEVEL'))
logger = logging.getLogger('load_data')


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver = PostgresSaver(pg_conn)

    logger.info('Start loading...')
    for data in sqlite_extractor.extract_data(chunk_size=1000):
        postgres_saver.save_data(data)
    logger.info('Done.')


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')
    }
    with sqlite_conn_context(os.environ.get('SQLITE_DB_PATH')) as sqlite_conn, \
            postgresql_conn_context(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
