import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN         = os.getenv("HF_TOKEN")
FASTAPI_URL      = os.getenv("FASTAPI_URL",
                              "http://localhost:8000")
OUTPUT_DIR       = os.getenv("OUTPUT_DIR", "outputs")
UPLOAD_DIR       = os.getenv("UPLOAD_DIR", "uploads")
MODEL_DIR        = os.getenv("MODEL_DIR", "models")
DEFAULT_DURATION = int(os.getenv("DEFAULT_DURATION", "30"))
SAMPLE_RATE      = int(os.getenv("DEFAULT_SAMPLE_RATE",
                                  "44100"))
MUSIC_MODEL      = os.getenv("MUSIC_MODEL",
                              "facebook/musicgen-small")
VOCAL_MODEL      = os.getenv("VOCAL_MODEL", "suno/bark")

# Supported genres
GENRES = [
    "Pop", "Rock", "Jazz", "Classical", "Hip-Hop",
    "Electronic", "Folk", "Country", "R&B", "Ambient",
    "Cinematic", "Lo-Fi", "Reggae", "Blues", "Metal"
]

# Supported moods
MOODS = [
    "Happy", "Sad", "Energetic", "Calm", "Romantic",
    "Mysterious", "Epic", "Motivational", "Melancholic",
    "Playful", "Tense", "Peaceful", "Dark", "Uplifting"
]

# Supported durations (seconds)
DURATIONS = [15, 30, 60, 90, 120]

# License info
LICENSE_INFO = {
    "model": "MusicGen (facebook/musicgen-small)",
    "license": "CC-BY-NC-4.0",
    "commercial_use": "Check model card for latest terms",
    "attribution": "Generated using Meta MusicGen",
    "copyright_status": "AI-generated — no human authorship"
}

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)