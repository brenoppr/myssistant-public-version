from routes.llm import llm_bp
from utils.test_utils import create_app

app = create_app()
app.register_blueprint(llm_bp)


def test_reset_chat_route(app):
    with app.test_client() as client:
        resp = client.get('/reset_chat')
    assert resp.status_code == 200
    assert resp.data == b'OK'

if __name__ == "__main__":
    test_reset_chat_route(app)