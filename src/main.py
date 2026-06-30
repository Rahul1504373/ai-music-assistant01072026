from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional, List
import os
from src.router import (
    generate_music_track,
    analyze_reference_style,
    generate_with_style
)
from src.engines.vocal_engine import vocal_engine
from src.config import OUTPUT_DIR, GENRES, MOODS, DURATIONS


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting AI Music Assistant...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Ready to generate music!")
    yield


app = FastAPI(
    title="AI Music Assistant",
    description=(
        "Generate copyright-free music using AI. "
        "Free for commercial use on YouTube/Instagram."
    ),
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated audio files
app.mount(
    "/outputs",
    StaticFiles(directory=OUTPUT_DIR),
    name="outputs"
)


class MusicRequest(BaseModel):
    prompt: str
    lyrics: Optional[str] = ""
    genre: str = "Pop"
    mood: str = "Happy"
    tempo: str = "medium"
    duration: int = 30
    instruments: Optional[List[str]] = []
    voice_preset: str = "female_1"
    include_vocals: bool = False
    use_for_youtube: bool = True


class StyleMusicRequest(BaseModel):
    prompt: str
    reference_features: dict
    duration: int = 30
    include_vocals: bool = False
    lyrics: Optional[str] = ""
    voice_preset: str = "female_1"


@app.get("/")
def root():
    return {
        "message": "AI Music Assistant API",
        "version": "1.0.0",
        "endpoints": [
            "/generate - Generate music from prompt",
            "/analyze-style - Analyze reference audio",
            "/generate-with-style - Generate in reference style",
            "/voices - Get available voice presets",
            "/options - Get genres, moods, durations",
            "/download/{filename} - Download generated music"
        ]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/options")
def get_options():
    return {
        "genres": GENRES,
        "moods": MOODS,
        "durations": DURATIONS,
        "tempos": ["slow", "medium", "fast", "very_fast"],
        "instruments": [
            "piano", "guitar", "drums", "bass",
            "violin", "saxophone", "synthesizer",
            "flute", "cello", "trumpet", "acoustic guitar",
            "electric guitar", "drum machine"
        ]
    }


@app.get("/voices")
def get_voices():
    return vocal_engine.get_available_voices()


@app.post("/generate")
async def generate_music(req: MusicRequest):
    """Generate original copyright-free music."""
    result = await generate_music_track(
        prompt=req.prompt,
        lyrics=req.lyrics,
        genre=req.genre,
        mood=req.mood,
        tempo=req.tempo,
        duration=req.duration,
        instruments=req.instruments or [],
        voice_preset=req.voice_preset,
        include_vocals=req.include_vocals,
        use_for_youtube=req.use_for_youtube
    )
    return result


@app.post("/analyze-style")
async def analyze_style(file: UploadFile):
    """Analyze musical style of reference audio."""
    if not file:
        return {"status": "error", "error": "No file uploaded"}

    allowed = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        return {
            "status": "error",
            "error": f"Unsupported format. Use: {allowed}"
        }

    audio_bytes = await file.read()
    result = await analyze_reference_style(
        audio_bytes, file.filename
    )
    return result


@app.post("/generate-with-style")
async def generate_styled_music(req: StyleMusicRequest):
    """Generate music inspired by reference style."""
    result = await generate_with_style(
        prompt=req.prompt,
        reference_features=req.reference_features,
        duration=req.duration,
        include_vocals=req.include_vocals,
        lyrics=req.lyrics,
        voice_preset=req.voice_preset
    )
    return result


@app.get("/download/{filename}")
async def download_music(filename: str):
    """Download a generated music file."""
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "error": "File not found"
        }
    return FileResponse(
        file_path,
        media_type="audio/wav",
        filename=filename
    )