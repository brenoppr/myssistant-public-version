from flask import Flask
from routes.tts import tts_bp
from routes.voice import voice_bp
from routes.upload import upload_bp
from routes.llm import llm_bp
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'sounds'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Blueprints
app.register_blueprint(tts_bp)
app.register_blueprint(voice_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(llm_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
