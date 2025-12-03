# src/db.py
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASS,
    "database": DB_NAME,
    "charset": "utf8mb4",
    "use_unicode": True,
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("DB connection error:", e)
        raise

def insert_article(article):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO articles (title, description, url, source, category, published_at, image_url)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE title = VALUES(title), description = VALUES(description)
    """
    vals = (
        article.get("title"),
        article.get("description"),
        article.get("url"),
        article.get("source"),
        article.get("category"),
        article.get("published_at"),
        article.get("image_url"),
    )
    try:
        cursor.execute(sql, vals)
        conn.commit()
        return True
    except Error as e:
        print("Insert error:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def fetch_latest(limit=20, category=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if category:
        cursor.execute(
            "SELECT * FROM articles WHERE category=%s ORDER BY published_at DESC LIMIT %s", (category, limit)
        )
    else:
        cursor.execute("SELECT * FROM articles ORDER BY published_at DESC LIMIT %s", (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
