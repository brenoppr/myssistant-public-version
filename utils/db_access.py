# utils/db_access.py
import sqlite3

def get_voice_by_name(name, db_path="voices.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT text, file_path FROM voices WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {'text': row[0], 'file_path': row[1]}
    return None

def list_voices(db_path="voices.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM voices")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result

def update_voice(name, new_text=None, new_file_path=None, db_path="voices.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if new_text and new_file_path:
        cursor.execute("UPDATE voices SET text = ?, file_path = ? WHERE name = ?", (new_text, new_file_path, name))
    elif new_text:
        cursor.execute("UPDATE voices SET text = ? WHERE name = ?", (new_text, name))
    elif new_file_path:
        cursor.execute("UPDATE voices SET file_path = ? WHERE name = ?", (new_file_path, name))
    conn.commit()
    conn.close()

def insert_voice(name, text, file_path, db_path="voices.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voices (name, text, file_path) VALUES (?, ?, ?)", (name, text, file_path))
    conn.commit()
    conn.close()
