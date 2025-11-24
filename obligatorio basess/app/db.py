import mysql.connector
from mysql.connector import Error
import config


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpassword",
        database="Obligatorio"
    )


def query_all(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()
    finally:
        conn.close()


def query_one(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, params or ())
            return cur.fetchone()
    finally:
        conn.close()


def execute(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            conn.commit()
            return cur.lastrowid
    finally:
        conn.close()
