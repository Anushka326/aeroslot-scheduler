import os

import mysql.connector

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "anushka"),
    "database": os.getenv("MYSQL_DATABASE", "airport_scheduler"),
}

def get_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

def dict_rows(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
