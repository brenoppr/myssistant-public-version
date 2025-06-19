from flask.testing import FlaskClient


def test_reset_chat_route(client: FlaskClient):
    resp = client.get('/reset_chat')
    assert resp.status_code == 200
    assert resp.data == b'OK'


