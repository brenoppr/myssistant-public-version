from flask import Blueprint, request, send_file
from utils.tts_utils import run

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/output.mp3', methods=['GET'])
def get_mp3():
    text = request.args.get('text')
    if not text:
        return "Missing 'text' parameter", 400
    audio_file = run(text)
    return send_file(audio_file, mimetype='audio/mpeg') if audio_file else ("Audio not found", 404)
