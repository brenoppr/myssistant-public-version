import io
import sqlite3
from functools import partial
from flask import Flask
from routes.transcription import transcription_bp
import utils.db_access as db_access


def create_app():
    app = Flask(__name__)
    app.register_blueprint(transcription_bp)
    return app


def _setup_db(tmp_path, with_voice=False):
    db_file = tmp_path / "voices.db"
    conn = sqlite3.connect(db_file)
    conn.execute(
        """CREATE TABLE voices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                text TEXT NOT NULL,
                file_path TEXT NOT NULL
            )"""
    )
    if with_voice:
        conn.execute(
            "INSERT INTO voices (name, text, file_path) VALUES (?, ?, ?)",
            ("voice", "old text", "old.wav"),
        )
    conn.commit()
    conn.close()
    return db_file


def _patch_db(monkeypatch, db_file):
    monkeypatch.setattr(
        db_access,
        "get_voice_by_name",
        partial(db_access.get_voice_by_name, db_path=str(db_file)),
    )
    monkeypatch.setattr(
        db_access,
        "update_voice",
        partial(db_access.update_voice, db_path=str(db_file)),
    )
    monkeypatch.setattr(
        db_access,
        "insert_voice",
        partial(db_access.insert_voice, db_path=str(db_file)),
    )


def _post_upload(client, data):
    return client.post("/upload", data=data, content_type="multipart/form-data")


def test_upload_creates_voice(monkeypatch, tmp_path):
    db_file = _setup_db(tmp_path)
    _patch_db(monkeypatch, db_file)
    audio_path = tmp_path / "file.wav"
    audio_path.write_bytes(b"data")
    monkeypatch.setattr(
        "routes.transcription.os.path.join", lambda a, b: str(tmp_path / b)
    )
    app = create_app()
    with app.test_client() as client:
        data = {"audio": (open(audio_path, "rb"), "file.wav"), "voice_name": "new"}
        resp = _post_upload(client, data)
    assert resp.status_code == 200
    js = resp.get_json()
    assert js["voice_name"] == "new"
    assert js["message"] == "Voice created successfully"
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("SELECT count(*) FROM voices WHERE name = 'new'")
    assert cur.fetchone()[0] == 1
    con.close()


def test_upload_updates_voice(monkeypatch, tmp_path):
    db_file = _setup_db(tmp_path, with_voice=True)
    _patch_db(monkeypatch, db_file)
    audio_path = tmp_path / "snd.wav"
    audio_path.write_bytes(b"abc")
    monkeypatch.setattr(
        "routes.transcription.os.path.join", lambda a, b: str(tmp_path / b)
    )
    app = create_app()
    with app.test_client() as client:
        data = {"audio": (open(audio_path, "rb"), "snd.wav"), "voice_name": "voice"}
        resp = _post_upload(client, data)
    assert resp.status_code == 200
    js = resp.get_json()
    assert js["message"] == "Voice updated successfully"
    con = sqlite3.connect(db_file)
    row = con.execute("SELECT file_path FROM voices WHERE name = 'voice'").fetchone()
    con.close()
    assert row[0].endswith("voice.wav")


def test_update_transcription_success(monkeypatch, tmp_path):
    db_file = _setup_db(tmp_path, with_voice=True)
    _patch_db(monkeypatch, db_file)
    app = create_app()
    with app.test_client() as client:
        resp = client.post(
            "/update_transcription",
            data={"voice_name": "voice", "transcription": "novo"},
        )
    assert resp.status_code == 200
    con = sqlite3.connect(db_file)
    text = con.execute("SELECT text FROM voices WHERE name = 'voice'").fetchone()[0]
    con.close()
    assert text == "novo"


def test_update_transcription_not_found(monkeypatch, tmp_path):
    db_file = _setup_db(tmp_path)
    _patch_db(monkeypatch, db_file)
    app = create_app()
    with app.test_client() as client:
        resp = client.post(
            "/update_transcription",
            data={"voice_name": "none", "transcription": "n"},
        )
    assert resp.status_code == 404

