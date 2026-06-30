import numpy as np
import soundfile as sf
import librosa
import os
from src.config import OUTPUT_DIR, SAMPLE_RATE


class AudioMixer:
    """
    Mixes music and vocals together into final output.
    Handles resampling, volume balancing, and export.
    """

    def mix_music_and_vocals(
        self,
        music_path: str,
        vocals_path: str,
        music_volume: float = 0.6,
        vocal_volume: float = 1.0,
        output_filename: str = "final_mix.wav"
    ) -> dict:
        """
        Mixes instrumental music with AI vocals.
        Returns path to final mixed audio file.
        """
        try:
            print("Mixing music and vocals...")

            # Load both audio files
            music, music_sr = librosa.load(
                music_path, sr=SAMPLE_RATE, mono=True
            )
            vocals, vocal_sr = librosa.load(
                vocals_path, sr=SAMPLE_RATE, mono=True
            )

            # Normalize lengths
            target_len = max(len(music), len(vocals))
            music = self._pad_or_trim(music, target_len)
            vocals = self._pad_or_trim(vocals, target_len)

            # Apply volume levels
            music = music * music_volume
            vocals = vocals * vocal_volume

            # Mix together
            mixed = music + vocals

            # Normalize to prevent clipping
            mixed = mixed / (np.max(np.abs(mixed)) + 1e-8)

            # Apply light compression
            mixed = self._apply_compression(mixed)

            # Save
            output_path = os.path.join(
                OUTPUT_DIR, output_filename
            )
            sf.write(output_path, mixed, SAMPLE_RATE)

            print(f"Mix saved to: {output_path}")

            return {
                "status": "success",
                "file_path": output_path,
                "filename": output_filename,
                "duration": len(mixed) / SAMPLE_RATE,
                "sample_rate": SAMPLE_RATE
            }

        except Exception as e:
            print(f"Mixing error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def export_final(
        self,
        audio_path: str,
        format: str = "wav",
        output_filename: str = "final.wav"
    ) -> dict:
        """Exports audio in specified format."""
        try:
            audio, sr = librosa.load(
                audio_path,
                sr=SAMPLE_RATE
            )
            output_path = os.path.join(
                OUTPUT_DIR,
                output_filename
            )
            sf.write(output_path, audio, sr)

            return {
                "status": "success",
                "file_path": output_path,
                "format": format
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _pad_or_trim(
        self,
        audio: np.ndarray,
        target_length: int
    ) -> np.ndarray:
        """Pads or trims audio to target length."""
        if len(audio) < target_length:
            padding = target_length - len(audio)
            return np.pad(audio, (0, padding))
        return audio[:target_length]

    def _apply_compression(
        self,
        audio: np.ndarray,
        threshold: float = 0.8
    ) -> np.ndarray:
        """
        Simple dynamic range compression.
        Reduces peaks and brings up quiet parts.
        """
        compressed = np.where(
            np.abs(audio) > threshold,
            threshold * np.sign(audio) + (
                audio - threshold * np.sign(audio)
            ) * 0.3,
            audio
        )
        return compressed


# Singleton instance
audio_mixer = AudioMixer()