import librosa
import numpy as np
import soundfile as sf
from io import BytesIO


class StyleAnalyzer:
    """
    Analyzes musical style features from a reference audio.
    IMPORTANT: This does NOT copy or sample the reference audio.
    It only extracts abstract musical features (tempo, key,
    energy) to guide generation of NEW original music.
    This is legally equivalent to a musician 'listening to'
    a song for inspiration — no copyright infringement.
    """

    def analyze(
        self,
        audio_bytes: bytes,
        filename: str = "reference.wav"
    ) -> dict:
        """
        Extracts musical style features from reference audio.
        Returns features that guide new music generation.
        """
        try:
            print("Analysing reference audio style...")

            # Load audio
            audio_data, sample_rate = librosa.load(
                BytesIO(audio_bytes),
                sr=None,
                mono=True
            )

            features = {}

            # 1. Tempo / BPM detection
            tempo, beats = librosa.beat.beat_track(
                y=audio_data,
                sr=sample_rate
            )
            features["tempo_bpm"] = float(tempo)
            features["tempo_category"] = self._categorize_tempo(
                float(tempo)
            )

            # 2. Key detection
            chroma = librosa.feature.chroma_cqt(
                y=audio_data,
                sr=sample_rate
            )
            key_idx = np.argmax(
                np.mean(chroma, axis=1)
            )
            keys = ['C', 'C#', 'D', 'D#', 'E', 'F',
                    'F#', 'G', 'G#', 'A', 'A#', 'B']
            features["key"] = keys[key_idx]

            # 3. Energy level
            rms = librosa.feature.rms(y=audio_data)
            features["energy_level"] = float(
                np.mean(rms)
            )
            features["energy_category"] = (
                "high" if features["energy_level"] > 0.1
                else "medium" if features["energy_level"] > 0.05
                else "low"
            )

            # 4. Spectral features (brightness/timbre)
            spectral_centroid = librosa.feature.spectral_centroid(
                y=audio_data, sr=sample_rate
            )
            features["brightness"] = float(
                np.mean(spectral_centroid)
            )

            # 5. Rhythm strength
            onset_env = librosa.onset.onset_strength(
                y=audio_data, sr=sample_rate
            )
            features["rhythm_strength"] = float(
                np.mean(onset_env)
            )

            # 6. Estimate genre from features
            features["estimated_genre"] = (
                self._estimate_genre(features)
            )

            # 7. Estimate mood from features
            features["estimated_mood"] = (
                self._estimate_mood(features)
            )

            # 8. Instrument hints
            features["instruments"] = (
                self._suggest_instruments(features)
            )

            # 9. Duration of reference
            features["reference_duration"] = (
                len(audio_data) / sample_rate
            )

            print(f"Style analysis complete: {features}")

            return {
                "status": "success",
                "features": features,
                "legal_note": (
                    "Only abstract musical features extracted. "
                    "No audio is copied or sampled. "
                    "Output will be completely new original music."
                )
            }

        except Exception as e:
            print(f"Style analysis error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "features": self._default_features()
            }

    def _categorize_tempo(self, bpm: float) -> str:
        if bpm < 70:
            return "slow"
        elif bpm < 100:
            return "medium"
        elif bpm < 130:
            return "fast"
        else:
            return "very_fast"

    def _estimate_genre(self, features: dict) -> str:
        """Estimates genre from musical features."""
        bpm = features.get("tempo_bpm", 100)
        energy = features.get("energy_level", 0.1)
        brightness = features.get("brightness", 2000)

        if bpm > 130 and energy > 0.1:
            return "Electronic"
        elif bpm > 120 and energy > 0.08:
            return "Rock"
        elif bpm < 80 and energy < 0.05:
            return "Classical"
        elif 80 <= bpm <= 110 and brightness > 2000:
            return "Pop"
        elif bpm < 90 and brightness < 1500:
            return "Jazz"
        elif energy < 0.04:
            return "Ambient"
        else:
            return "Pop"

    def _estimate_mood(self, features: dict) -> str:
        """Estimates mood from musical features."""
        energy = features.get("energy_level", 0.1)
        brightness = features.get("brightness", 2000)
        bpm = features.get("tempo_bpm", 100)

        if energy > 0.1 and bpm > 120:
            return "Energetic"
        elif energy < 0.05 and bpm < 80:
            return "Calm"
        elif brightness > 2500:
            return "Happy"
        elif brightness < 1500:
            return "Melancholic"
        else:
            return "Neutral"

    def _suggest_instruments(
        self, features: dict
    ) -> list:
        """Suggests instruments based on musical features."""
        genre = features.get("estimated_genre", "Pop")
        instrument_map = {
            "Pop":        ["piano", "guitar", "drums",
                           "synthesizer"],
            "Rock":       ["electric guitar", "drums",
                           "bass guitar"],
            "Jazz":       ["saxophone", "piano",
                           "double bass", "drums"],
            "Classical":  ["violin", "piano", "cello",
                           "flute"],
            "Electronic": ["synthesizer", "drum machine",
                           "bass"],
            "Ambient":    ["synthesizer", "piano",
                           "soft pads"],
            "Hip-Hop":    ["drums", "bass", "synthesizer"],
            "Country":    ["acoustic guitar", "fiddle",
                           "banjo"],
        }
        return instrument_map.get(
            genre,
            ["piano", "guitar", "drums"]
        )

    def _default_features(self) -> dict:
        return {
            "tempo_bpm": 100,
            "tempo_category": "medium",
            "key": "C",
            "energy_level": 0.1,
            "energy_category": "medium",
            "brightness": 2000,
            "rhythm_strength": 1.0,
            "estimated_genre": "Pop",
            "estimated_mood": "Happy",
            "instruments": ["piano", "guitar", "drums"]
        }


# Singleton instance
style_analyzer = StyleAnalyzer()