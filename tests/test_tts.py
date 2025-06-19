from flask.testing import FlaskClient


def test_get_mp3_requires_text(client: FlaskClient):
    resp = client.get('/output.mp3')
    assert resp.status_code == 400


def test_get_mp3_with_text(client: FlaskClient):
    resp = client.get('/output.mp3?text=ola')
    assert resp.status_code in (200, 404)

