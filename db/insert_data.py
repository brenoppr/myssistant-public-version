# db/insert_data.py
import sqlite3

data = {"default_voice": ("Esse é um áudio padrão gravado para demonstrar a funcionalidade mínima da aplicação.", "sounds/default_voice.wav")}

conn = sqlite3.connect("voices.db")
cursor = conn.cursor()
for name, (text, path) in data.items():
    cursor.execute("INSERT INTO voices (name, text, file_path) VALUES (?, ?, ?)", (name, text, path))
conn.commit()
conn.close()
