from utils.test_utils import create_app
from routes.tts import tts_bp


app = create_app()
app.register_blueprint(tts_bp)

def test_get_mp3_requires_text(app):
    with app.test_client() as client:
        resp = client.get('/output.mp3')
    assert resp.status_code == 400


def test_get_mp3_with_text(app):
    with app.test_client() as client:
        resp = client.get('/output.mp3?text=ola')
    assert resp.status_code in (200, 404)
