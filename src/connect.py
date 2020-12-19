# encoding: UTF-8

import argparse

# Драйвер PostgreSQL
# Находится в модуле psycopg2-binary, который можно установить командой
# pip install psycopg2-binary или её аналогом.
import psycopg2 as pg_driver
# Драйвер SQLite3
# Находится в модуле sqlite3, который можно установить командой
# pip install sqlite3 или её аналогом.
import sqlite3 as sqlite_driver
from psycopg2 import pool


# Разбирает аргументы командной строки.
# Выплевывает структуру с полями, соответствующими каждому аргументу.
def parse_cmd_line():
    parser = argparse.ArgumentParser(description='Эта программа вычисляет 2+2 при помощи реляционной СУБД')
    parser.add_argument('--pg-host', help='PostgreSQL host name', default='localhost')
    parser.add_argument('--pg-port', help='PostgreSQL port', default=5432)
    parser.add_argument('--pg-user', help='PostgreSQL user', default='')
    parser.add_argument('--pg-password', help='PostgreSQL password', default='')
    parser.add_argument('--pg-database', help='PostgreSQL database', default='')
    parser.add_argument('--sqlite-file', help='SQLite3 database file. Type :memory: to use in-memory SQLite3 database',
                        default='sqlite.db')

    return parser.parse_args()
# --pg-host=127.0.0.1 --pg-port=5432 --pg-user=postgres --pg-password=lj,hsqpostgresql --pg-database=postgres
# user='postgres',
#                                    password="lj,hsqpostgresql",
#                                    host='127.0.0.1',
#                                    port='5432',
#                                    database='postgres'