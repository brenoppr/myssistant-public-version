from flask import Flask
from routes.gemini import gemini_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(gemini_bp)
    return app


def test_reset_chat_route():
    app = create_app()
    with app.test_client() as client:
        resp = client.get('/reset_chat')
    assert resp.status_code == 200
    assert resp.data == b'OK'
