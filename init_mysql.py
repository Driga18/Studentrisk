import os
import pymysql
from app import app
from databaseOJ import db

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Tanatswa@1212")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "studentdb")

conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    port=MYSQL_PORT,
    autocommit=True,
)

try:
    with conn.cursor() as cursor:
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}')
    print('DATABASE_CREATED_OR_EXISTS')
finally:
    conn.close()

with app.app_context():
    db.create_all()
    print('TABLES_READY')
