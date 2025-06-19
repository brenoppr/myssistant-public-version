import os
import sys
import pytest

# Ensure project root is on sys.path for imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.test_utils import create_app
from routes.llm import llm_bp
from routes.tts import tts_bp

@pytest.fixture
def app():
    app = create_app()
    app.register_blueprint(llm_bp)
    app.register_blueprint(tts_bp)
    return app
