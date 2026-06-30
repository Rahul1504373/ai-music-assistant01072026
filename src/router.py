import os
import uuid
from src.engines.music_engine import music_engine
from src.engines.vocal_engine import vocal_engine
from src.engines.style_analyzer import style_analyzer
from src.engines.audio_mixer import audio_mixer
from src.processors.prompt_processor import prompt_processor
from src.config import OUTPUT_DIR


async def generate_music_track(
    prompt: str,
    lyrics: str,
    genre: str,
    mood: str,
    tempo: str,
    duration: int,
    instruments: list,
    voice_preset: str,
    include_vocals: bool,
    use_for_youtube: bool
) -> dict:
    """
    Main music generation pipeline.
    Orchestrates all engines to create final music.
    """
    session_id = str(uuid.uuid4())[:8]
    results = {}

    try:
        # Step 1: Enhance prompt
        enhanced_prompt = prompt_processor.enhance_prompt(
            prompt, genre, mood, use_for_youtube
        )

        # Step 2: Generate instrumental music
        print(f"[{session_id}] Generating music...")
        music_result = music_engine.generate_music(
            prompt=enhanced_prompt,
            duration=duration,
            genre=genre,
            mood=mood,
            tempo=tempo,
            instruments=instruments,
            output_filename=f"music_{session_id}.wav"
        )
        results["music"] = music_result

        if music_result["status"] != "success":
            return {
                "status": "error",
                "error": "Music generation failed",
                "details": music_result
            }

        final_path = music_result["file_path"]

        # Step 3: Generate vocals if requested
        if include_vocals and lyrics:
            print(f"[{session_id}] Generating vocals...")

            # Validate lyrics
            lyrics_check = prompt_processor.validate_lyrics(
                lyrics
            )
            if not lyrics_check["valid"]:
                print(
                    f"Lyrics issue: {lyrics_check['error']}"
                )
                include_vocals = False
            else:
                vocal_result = vocal_engine.generate_vocals(
                    lyrics=lyrics_check["cleaned_lyrics"],
                    voice_preset=voice_preset,
                    output_filename=f"vocals_{session_id}.wav"
                )
                results["vocals"] = vocal_result

                # Step 4: Mix if vocals succeeded
                if vocal_result["status"] == "success":
                    print(
                        f"[{session_id}] Mixing tracks..."
                    )
                    mix_result = audio_mixer.mix_music_and_vocals(
                        music_path=music_result["file_path"],
                        vocals_path=vocal_result["file_path"],
                        output_filename=(
                            f"final_mix_{session_id}.wav"
                        )
                    )
                    results["mix"] = mix_result

                    if mix_result["status"] == "success":
                        final_path = mix_result["file_path"]

        return {
            "status": "success",
            "session_id": session_id,
            "final_audio_path": final_path,
            "final_filename": os.path.basename(final_path),
            "details": results,
            "metadata": {
                "prompt": prompt,
                "enhanced_prompt": enhanced_prompt,
                "genre": genre,
                "mood": mood,
                "duration": duration,
                "has_vocals": include_vocals and bool(lyrics),
                "voice_preset": (
                    voice_preset if include_vocals else None
                ),
                "license": "See model card for latest terms",
                "copyright_note": (
                    "AI-generated music. "
                    "Verify commercial use terms before "
                    "publishing on YouTube/Instagram."
                )
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "session_id": session_id
        }


async def analyze_reference_style(
    audio_bytes: bytes,
    filename: str
) -> dict:
    """Analyzes style of reference audio file."""
    return style_analyzer.analyze(audio_bytes, filename)


async def generate_with_style(
    prompt: str,
    reference_features: dict,
    duration: int,
    include_vocals: bool,
    lyrics: str,
    voice_preset: str
) -> dict:
    """Generates music inspired by reference style."""
    session_id = str(uuid.uuid4())[:8]

    try:
        music_result = (
            music_engine.generate_with_style_reference(
                prompt=prompt,
                reference_features=reference_features,
                duration=duration,
                output_filename=f"styled_{session_id}.wav"
            )
        )

        final_path = music_result.get("file_path", "")

        if (include_vocals and lyrics
                and music_result["status"] == "success"):
            vocal_result = vocal_engine.generate_vocals(
                lyrics=lyrics,
                voice_preset=voice_preset,
                output_filename=f"vocals_styled_{session_id}.wav"
            )

            if vocal_result["status"] == "success":
                mix_result = audio_mixer.mix_music_and_vocals(
                    music_path=music_result["file_path"],
                    vocals_path=vocal_result["file_path"],
                    output_filename=(
                        f"styled_mix_{session_id}.wav"
                    )
                )
                if mix_result["status"] == "success":
                    final_path = mix_result["file_path"]

        return {
            "status": "success",
            "final_audio_path": final_path,
            "final_filename": os.path.basename(final_path),
            "session_id": session_id,
            "legal_note": (
                "Output is 100% new original music. "
                "Reference audio was only used for "
                "style feature extraction — "
                "no audio was copied or sampled."
            )
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}