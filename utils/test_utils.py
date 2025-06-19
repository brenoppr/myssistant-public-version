from flask import Flask
import os


def create_app() -> Flask:
    """Create a barebones Flask application for testing."""
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return Flask(__name__, root_path=root_path)

