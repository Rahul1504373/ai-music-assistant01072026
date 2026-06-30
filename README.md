# 🎵 AI Music Assistant

An end-to-end GenAI system that generates **original, copyright-free music**
from text prompts — including optional AI-synthesized vocals — running
entirely on **free, open-source models** with **zero infrastructure cost**.

---

## 🎯 What It Does

- Generate instrumental music from a text description (genre, mood, tempo, instruments)
- Add AI-synthesized singing vocals from custom lyrics
- Upload a reference song to extract its musical *style* (tempo, key, energy)
  and generate **new original music** inspired by that style — no audio is
  copied or sampled
- Download the final track as a `.wav` file, ready for YouTube/Instagram

---

## 🏗️ Architecture
Streamlit UI (port 8501)
|
v  HTTP POST
FastAPI backend (port 8000)
|
+----+----+----------------+
|         |                |
Music      Vocal          Style
Engine     Engine         Analyzer
(MusicGen) (Bark TTS)     (librosa)
|         |                |
+----+----+----------------+
|
Audio Mixer
|
final_mix.wav

---

## 🛠️ Tech Stack

| Component | Tool | License |
|---|---|---|
| Frontend | Streamlit | Apache 2.0 |
| Backend | FastAPI + Uvicorn | MIT |
| Music generation | MusicGen (`facebook/musicgen-small`) | CC-BY-NC-4.0 |
| Vocal synthesis | Bark (Suno AI) | MIT |
| Style analysis | librosa | ISC |
| Audio I/O | soundfile, numpy | BSD |

> ⚠️ MusicGen is licensed CC-BY-NC-4.0. Verify the latest model card
> on HuggingFace before any commercial use.

---

## 🚀 Setup

### Prerequisites
- Python 3.11
- Free HuggingFace account ([get a token](https://huggingface.co/settings/tokens) —
  Fine-grained, with "Make calls to Inference Providers" enabled)

### Install

```bash
git clone https://github.com/Rahul1504373/ai-music-assistant01072026.git
cd ai-music-assistant01072026

python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
pip install git+https://github.com/suno-ai/bark.git --no-deps
pip install encodec funcy nltk
```

### Configure

Create a `.env` file:

```env
HF_TOKEN=hf_your_token_here
FASTAPI_URL=http://localhost:8000
OUTPUT_DIR=outputs
UPLOAD_DIR=uploads
MODEL_DIR=models
DEFAULT_DURATION=30
DEFAULT_SAMPLE_RATE=44100
MUSIC_MODEL=facebook/musicgen-small
VOCAL_MODEL=suno/bark
```

### Run

**Terminal 1:**
```bash
$env:PYTHONPATH = "."
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2:**
```bash
$env:PYTHONPATH = "."
streamlit run src/app.py
```

Open **http://localhost:8501**

---

## ⏱️ Performance Notes

- Runs entirely on **CPU** — no GPU required
- First generation downloads the model (~2.4 GB, one-time)
- 15s of music takes ~1–4 minutes on CPU after the model is cached
- Vocal generation (Bark) adds 2–5 minutes per track

---

## ⚖️ Copyright & Legal

AI-generated output has no human author and is generally not subject to
traditional copyright claims. However:

- **MusicGen-small is CC-BY-NC-4.0** — non-commercial use only unless
  license terms are verified to have changed
- **Bark voices** are 100% synthetic — no real person is cloned
- For guaranteed commercial/monetized use, verify the current model
  license or use a service with an explicit commercial license
  (e.g. Riffusion, Apache 2.0)

---

## 📁 Project Structure
src/
├── app.py                    # Streamlit UI
├── main.py                   # FastAPI endpoints
├── config.py                 # Settings & env vars
├── router.py                 # Orchestrates generation pipeline
├── engines/
│   ├── music_engine.py       # MusicGen integration
│   ├── vocal_engine.py       # Bark TTS integration
│   ├── style_analyzer.py     # librosa feature extraction
│   └── audio_mixer.py        # Mix music + vocals
└── processors/
└── prompt_processor.py   # Prompt enhancement & lyrics validation

---

## 👨‍💻 Author

**Rahul Girdhar**
[GitHub](https://github.com/Rahul1504373) ·
[LinkedIn](https://linkedin.com/in/rahul-girdhar2903)