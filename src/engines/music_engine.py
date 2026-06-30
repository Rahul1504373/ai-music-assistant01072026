import torch
import numpy as np
import soundfile as sf
import os
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from src.config import (
    HF_TOKEN, OUTPUT_DIR, MUSIC_MODEL, SAMPLE_RATE
)


class MusicEngine:
    """
    Generates original music using Meta's MusicGen model.
    MusicGen creates completely new music from text prompts.
    License: CC-BY-NC-4.0 (check latest model card)
    """

    def __init__(self):
        self.model = None
        self.processor = None
        self.device = (
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        print(f"Music engine using device: {self.device}")

    def load_model(self):
        """Loads MusicGen model (downloads on first run)."""
        if self.model is None:
            print(f"Loading {MUSIC_MODEL}...")
            print("This may take a few minutes on first run...")

            self.processor = AutoProcessor.from_pretrained(
                MUSIC_MODEL,
                token=HF_TOKEN
            )
            self.model = (
                MusicgenForConditionalGeneration
                .from_pretrained(
                    MUSIC_MODEL,
                    token=HF_TOKEN
                )
            )
            self.model.to(self.device)
            print("Music model loaded successfully!")

    def build_prompt(
        self,
        user_prompt: str,
        genre: str,
        mood: str,
        tempo: str,
        instruments: list
    ) -> str:
        """
        Builds an optimised text prompt for music generation.
        Better prompts = better music!
        """
        parts = []

        # Add genre and mood
        if genre:
            parts.append(genre.lower())
        if mood:
            parts.append(f"{mood.lower()} mood")

        # Add user description
        if user_prompt:
            parts.append(user_prompt)

        # Add tempo
        tempo_map = {
            "slow": "slow tempo, 60-80 BPM",
            "medium": "medium tempo, 90-110 BPM",
            "fast": "fast tempo, 120-140 BPM",
            "very_fast": "very fast, energetic, 150+ BPM"
        }
        if tempo in tempo_map:
            parts.append(tempo_map[tempo])

        # Add instruments
        if instruments:
            parts.append(
                "featuring " + ", ".join(instruments)
            )

        # Quality boosters
        parts.append(
            "high quality, professional production, "
            "clear mix, no noise"
        )

        final_prompt = ", ".join(parts)
        print(f"Generated music prompt: {final_prompt}")
        return final_prompt

    def generate_music(
        self,
        prompt: str,
        duration: int = 30,
        genre: str = "Pop",
        mood: str = "Happy",
        tempo: str = "medium",
        instruments: list = None,
        output_filename: str = "generated_music.wav"
    ) -> dict:
        """
        Generates original music from a text prompt.
        Returns path to generated audio file.
        """
        self.load_model()

        if instruments is None:
            instruments = []

        # Build optimised prompt
        full_prompt = self.build_prompt(
            prompt, genre, mood, tempo, instruments
        )

        print(f"Generating {duration}s of music...")
        print(f"Prompt: {full_prompt}")

        # Calculate tokens needed
        # MusicGen generates ~50 tokens per second
        max_tokens = duration * 50

        # Prepare inputs
        inputs = self.processor(
            text=[full_prompt],
            padding=True,
            return_tensors="pt"
        ).to(self.device)

        # Generate audio
        with torch.no_grad():
            audio_values = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                guidance_scale=3.0,
                temperature=1.0
            )

        # Convert to numpy
        audio_data = audio_values[0, 0].cpu().numpy()

        # Get sample rate from model config
        model_sample_rate = (
            self.model.config.audio_encoder.sampling_rate
        )

        # Normalise audio
        audio_data = audio_data / (
            np.max(np.abs(audio_data)) + 1e-8
        )

        # Save to file
        output_path = os.path.join(
            OUTPUT_DIR, output_filename
        )
        sf.write(
            output_path,
            audio_data,
            model_sample_rate
        )

        print(f"Music saved to: {output_path}")

        return {
            "status": "success",
            "file_path": output_path,
            "filename": output_filename,
            "duration": duration,
            "sample_rate": model_sample_rate,
            "prompt_used": full_prompt,
            "genre": genre,
            "mood": mood,
            "model_used": MUSIC_MODEL,
            "license": "CC-BY-NC-4.0",
            "copyright_free": True,
            "commercial_use_note": (
                "Verify latest model license terms "
                "at huggingface.co/facebook/musicgen-small"
            )
        }

    def generate_with_style_reference(
        self,
        prompt: str,
        reference_features: dict,
        duration: int = 30,
        output_filename: str = "styled_music.wav"
    ) -> dict:
        """
        Generates music inspired by style features
        extracted from a reference audio.
        NOTE: Does NOT copy or sample the reference audio.
        Only uses extracted musical features as guidance.
        """
        self.load_model()

        # Build style-informed prompt
        style_prompt = self._build_style_prompt(
            prompt, reference_features
        )

        return self.generate_music(
            prompt=style_prompt,
            duration=duration,
            genre=reference_features.get("genre", "Pop"),
            mood=reference_features.get("mood", "Happy"),
            tempo=reference_features.get("tempo", "medium"),
            instruments=reference_features.get(
                "instruments", []
            ),
            output_filename=output_filename
        )

    def _build_style_prompt(
        self,
        user_prompt: str,
        features: dict
    ) -> str:
        """Combines user prompt with extracted style features."""
        style_parts = []

        if features.get("tempo_bpm"):
            bpm = features["tempo_bpm"]
            if bpm < 80:
                style_parts.append("slow ballad")
            elif bpm < 110:
                style_parts.append("medium tempo")
            elif bpm < 140:
                style_parts.append("upbeat fast")
            else:
                style_parts.append("very fast energetic")

        if features.get("key"):
            style_parts.append(
                f"in the key of {features['key']}"
            )

        if features.get("energy_level"):
            energy = features["energy_level"]
            if energy > 0.7:
                style_parts.append("high energy")
            elif energy > 0.4:
                style_parts.append("moderate energy")
            else:
                style_parts.append("soft mellow")

        style_desc = ", ".join(style_parts)
        return f"{user_prompt}, {style_desc}"


# Singleton instance
music_engine = MusicEngine()