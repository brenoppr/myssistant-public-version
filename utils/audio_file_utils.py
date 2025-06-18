import os

def save_uploaded_audio(file_storage, voice_name, base_dir="sounds"):
    os.makedirs(base_dir, exist_ok=True)
    audio_path = os.path.join(base_dir, f"{voice_name}.wav")
    file_storage.save(audio_path)
    return audio_path

def check_audio_exists(path):
    return os.path.exists(path)