import sqlite3
import os

def init_db(db_path="voices.db"):
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE voices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                text TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

if __name__ == "__main__":
    init_db()
