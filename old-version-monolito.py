import os
import re
from pathlib import Path
import numpy as np
import soundfile as sf
from flask import Flask, request, send_file, jsonify


app = Flask(__name__)

VOICE_NAME = 'default_voice'
def initialize_model():
    "Placeholder para inicialização do modelo."
    return True

def generate_audio(text):
    "Placeholder para geração do áudio."
    return "output/generated_audio.wav"

def run(text):
    # Main entry point
    model_initialized = initialize_model()

    output_file = generate_audio(text)
    if model_initialized:
        return output_file


app = Flask(__name__)

@app.route('/output.mp3', methods=['GET'])
def get_mp3():
    # Extract 'text' from the query parameters
    text = request.args.get('text')

    if not text:
        return "Missing 'text' parameter", 400

    # Call the run(text) function to generate the mp3 file
    print("Received text:", text)
    audio_file = run(text)
    # audio_file="/content/drive/MyDrive/TelecomVozes/arquivo1.mp3"
    print("Generated audio file:", audio_file)
    # Send the generated mp3 file as a response
    if os.path.exists(audio_file):
        return send_file(audio_file, mimetype='audio/mpeg')
    else:
        return "Audio file not found", 404


@app.route('/reset_chat', methods=['GET'])
def reset_llm_chat():
    "Placeholder function for resetting the chat history."
    return "OK", 200

@app.route('/vozes', methods=['GET'])
def vozes_disponiveis():
    return [key for key in vozes.vozes_dict.keys()], 200


UPLOAD_FOLDER = 'sounds'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to transcribe audio using SpeechRecognition
def transcribe_audio(audio_path):
    "Placeholder para a função de transcrever áudio"
    return "Esse é um áudio de exemplo para mostrar o funcionamento do aplicativo."



@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    file_name = request.form.get('file_name', 'audio_file')
    
    # Save the audio file
    audio_path = os.path.join(UPLOAD_FOLDER, f'{file_name}.wav')
    audio_file.save(audio_path)
    
    # Transcribe the audio file
    transcription = transcribe_audio(audio_path)
    
    # Save the transcription to a text file
    transcription_path = os.path.join(UPLOAD_FOLDER, f'{file_name}.txt')
    with open(transcription_path, 'w') as f:
        f.write(transcription)
    
    return jsonify({
        'message': 'File uploaded and transcribed successfully',
        'audio_path': audio_path,
        'transcription_path': transcription_path,
        'transcription': transcription
    }), 200



# TO BE DONE
@app.route('/update_transcription', methods=['POST'])
def update_transcription():
    # Save the transcription to a text file
    transcription_path = os.path.join(UPLOAD_FOLDER, f'{file_name}.txt')
    with open(transcription_path, 'w') as f:
        f.write(transcription)
    
    return jsonify({
        'message': 'File uploaded and transcribed successfully',
        'audio_path': audio_path,
        'transcription_path': transcription_path,
        'transcription': transcription
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
