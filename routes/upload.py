from flask import Blueprint, request, jsonify
from utils.transcription_utils import transcribe_audio
from utils.db_access import get_voice_by_name, update_voice, insert_voice
from utils.audio_file_utils import save_uploaded_audio

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    voice_name = request.form.get('file_name')
    if not voice_name:
        return jsonify({'error': 'Missing file_name'}), 400

    audio_path = save_uploaded_audio(request.files['audio'], voice_name)
    transcription = transcribe_audio(audio_path)

    if get_voice_by_name(voice_name):
        update_voice(name=voice_name, new_text=transcription, new_file_path=audio_path)
        message = 'Voice updated successfully'
    else:
        insert_voice(name=voice_name, text=transcription, file_path=audio_path)
        message = 'Voice created successfully'

    return jsonify({
        'message': message,
        'voice_name': voice_name,
        'audio_path': audio_path,
        'transcription': transcription
    }), 200

@upload_bp.route('/update_transcription', methods=['POST'])
def update_transcription():
    voice_name = request.form.get('voice_name')
    transcription = request.form.get('transcription')

    if not voice_name or not transcription:
        return jsonify({'error': 'Missing parameters'}), 400
    if not get_voice_by_name(voice_name):
        return jsonify({'error': 'Voice not found'}), 404

    update_voice(name=voice_name, new_text=transcription)
    return jsonify({'message': 'Transcript updated successfully'}), 200
    