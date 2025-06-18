import sqlite3
from functools import partial
from flask import Flask
from routes.voice import voice_bp
import utils.db_access as db_access


def create_app():
    app = Flask(__name__)
    app.register_blueprint(voice_bp)
    return app


def _setup_db(tmp_path):
    db_file = tmp_path / 'voices.db'
    conn = sqlite3.connect(db_file)
    conn.execute('''CREATE TABLE voices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        text TEXT NOT NULL,
                        file_path TEXT NOT NULL
                    )''')
    conn.execute("INSERT INTO voices (name, text, file_path) VALUES ('a','x','f')")
    conn.execute("INSERT INTO voices (name, text, file_path) VALUES ('b','y','f2')")
    conn.commit()
    conn.close()
    return db_file


def _patch_list(monkeypatch, db_file):
    monkeypatch.setattr(
        db_access,
        'list_voices',
        partial(db_access.list_voices, db_path=str(db_file))
    )


def test_vozes_disponiveis(monkeypatch, tmp_path):
    db_file = _setup_db(tmp_path)
    _patch_list(monkeypatch, db_file)
    app = create_app()
    with app.test_client() as client:
        resp = client.get('/vozes')
    assert resp.status_code == 200
    assert resp.get_json() == ['a', 'b']
