import base64
from flask import Blueprint, request, jsonify
from utils.db_access import get_voice_by_name, list_voices
from utils.audio_file_utils import check_audio_exists

voice_bp = Blueprint('voice', __name__)

@voice_bp.route('/vozes', methods=['GET'])
def vozes_disponiveis():
    return jsonify(list_voices()), 200

@voice_bp.route('/recuperar_voz', methods=['GET'])
def recuperar_voz():
    voice_name = request.args.get('voice_name')
    if not voice_name:
        return jsonify({'error': 'Missing voice_name parameter'}), 400

    voice_data = get_voice_by_name(voice_name)
    if not voice_data:
        return jsonify({'error': 'Voice not found'}), 404

    audio_path = voice_data['file_path']
    transcription = voice_data['text']

    if not check_audio_exists(audio_path):
        return jsonify({'error': 'Audio file not found'}), 404

    with open(audio_path, 'rb') as f:
        audio_base64 = base64.b64encode(f.read()).decode('utf-8')

    return jsonify({
        'voice_name': voice_name,
        'transcription': transcription,
        'audio_base64': audio_base64
    }), 200
