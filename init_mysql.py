import pymysql
from app import app
from databaseOJ import db

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='Tanatswa@1212',
    port=3306,
    autocommit=True,
)

try:
    with conn.cursor() as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS studentdb')
    print('DATABASE_CREATED_OR_EXISTS')
finally:
    conn.close()

with app.app_context():
    db.create_all()
    print('TABLES_READY')
