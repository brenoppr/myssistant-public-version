from flask import Flask
from routes.tts import tts_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(tts_bp)
    return app


def test_get_mp3_requires_text():
    app = create_app()
    with app.test_client() as client:
        resp = client.get('/output.mp3')
    assert resp.status_code == 400


def test_get_mp3_with_text():
    app = create_app()
    with app.test_client() as client:
        resp = client.get('/output.mp3?text=ola')
    assert resp.status_code in (200, 404)
