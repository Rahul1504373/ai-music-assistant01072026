import numpy as np
import os
import soundfile as sf
from src.config import OUTPUT_DIR, HF_TOKEN


class VocalEngine:
    """
    Generates AI vocals using Bark (by Suno AI).
    Bark is MIT licensed — free for commercial use.
    Generates completely synthetic voices — no real person cloned.
    """

    # Available voice presets (all synthetic, no real people)
    VOICE_PRESETS = {
        "male_1":   "v2/en_speaker_0",
        "male_2":   "v2/en_speaker_1",
        "male_3":   "v2/en_speaker_2",
        "female_1": "v2/en_speaker_3",
        "female_2": "v2/en_speaker_4",
        "female_3": "v2/en_speaker_5",
        "male_4":   "v2/en_speaker_6",
        "female_4": "v2/en_speaker_7",
        "male_5":   "v2/en_speaker_8",
        "female_5": "v2/en_speaker_9",
    }

    def __init__(self):
        self.model = None
        self.preprocess = None
        self._loaded = False

    def load_model(self):
        """Loads Bark TTS model."""
        if not self._loaded:
            try:
                from bark import SAMPLE_RATE, generate_audio
                from bark import preload_models
                print("Loading Bark vocal model...")
                preload_models()
                self._loaded = True
                print("Bark model loaded!")
            except ImportError:
                print(
                    "Bark not installed. "
                    "Installing via pip..."
                )
                os.system("pip install bark")
                from bark import preload_models
                preload_models()
                self._loaded = True

    def generate_vocals(
        self,
        lyrics: str,
        voice_preset: str = "female_1",
        output_filename: str = "vocals.wav"
    ) -> dict:
        """
        Generates AI vocals from lyrics text.
        Uses completely synthetic AI voices.
        No real person's voice is used or cloned.
        """
        try:
            from bark import SAMPLE_RATE, generate_audio

            self.load_model()

            # Get voice preset
            preset = self.VOICE_PRESETS.get(
                voice_preset,
                "v2/en_speaker_3"
            )

            # Add singing cues to improve vocal quality
            singing_lyrics = self._format_for_singing(lyrics)

            print(
                f"Generating vocals with "
                f"voice: {voice_preset}..."
            )

            # Generate audio
            audio_array = generate_audio(
                singing_lyrics,
                history_prompt=preset
            )

            # Save vocals
            output_path = os.path.join(
                OUTPUT_DIR, output_filename
            )
            sf.write(output_path, audio_array, SAMPLE_RATE)

            print(f"Vocals saved to: {output_path}")

            return {
                "status": "success",
                "file_path": output_path,
                "filename": output_filename,
                "voice_used": voice_preset,
                "sample_rate": SAMPLE_RATE,
                "license": "MIT",
                "copyright_free": True,
                "voice_note": (
                    "100% synthetic AI voice — "
                    "no real person cloned"
                )
            }

        except Exception as e:
            print(f"Vocal generation error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "fallback": "instrumental_only"
            }

    def _format_for_singing(self, lyrics: str) -> str:
        """
        Formats lyrics for better Bark singing output.
        Adds musical notation hints.
        """
        # Add singing indicator
        formatted = "♪ " + lyrics + " ♪"

        # Replace line breaks with musical pauses
        formatted = formatted.replace("\n\n", " ... ")
        formatted = formatted.replace("\n", " ♪ ")

        return formatted

    def get_available_voices(self) -> dict:
        """Returns all available synthetic voice presets."""
        return {
            "male_voices": [
                k for k in self.VOICE_PRESETS.keys()
                if "male" in k
            ],
            "female_voices": [
                k for k in self.VOICE_PRESETS.keys()
                if "female" in k
            ],
            "all_voices": list(self.VOICE_PRESETS.keys()),
            "note": (
                "All voices are 100% synthetic AI voices. "
                "No real person's voice is used."
            )
        }


# Singleton instance
vocal_engine = VocalEngine()