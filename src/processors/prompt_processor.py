class PromptProcessor:
    """
    Enhances user prompts for better music generation.
    Adds technical music descriptors to improve output quality.
    """

    GENRE_DESCRIPTORS = {
        "Pop":       "catchy melody, verse-chorus structure, "
                     "radio-friendly",
        "Rock":      "guitar riffs, powerful drums, distortion",
        "Jazz":      "improvisation, swing rhythm, "
                     "complex chords",
        "Classical": "orchestral, dynamic range, "
                     "structured composition",
        "Hip-Hop":   "strong beat, bass heavy, rhythmic",
        "Electronic":"synthesizer leads, four-on-the-floor, "
                     "electronic production",
        "Folk":      "acoustic instruments, storytelling, "
                     "natural sound",
        "Ambient":   "atmospheric, slow evolving, "
                     "meditative texture",
        "Lo-Fi":     "warm vinyl sound, subtle imperfections, "
                     "relaxing",
        "Cinematic": "orchestral, emotional, "
                     "movie soundtrack quality",
    }

    MOOD_DESCRIPTORS = {
        "Happy":       "major key, bright tone, uplifting",
        "Sad":         "minor key, slow, emotional, melancholic",
        "Energetic":   "fast tempo, driving rhythm, "
                       "high energy",
        "Calm":        "gentle, soft dynamics, peaceful",
        "Romantic":    "warm harmonies, smooth, "
                       "emotional depth",
        "Mysterious":  "minor tonality, sparse, "
                       "atmospheric tension",
        "Epic":        "large orchestration, "
                       "powerful crescendos, dramatic",
        "Motivational":"rising melody, empowering, "
                       "triumphant",
    }

    def enhance_prompt(
        self,
        user_prompt: str,
        genre: str,
        mood: str,
        use_for_youtube: bool = True
    ) -> str:
        """
        Enhances the user prompt with music descriptors
        for better generation quality.
        """
        parts = [user_prompt]

        # Add genre-specific descriptors
        if genre in self.GENRE_DESCRIPTORS:
            parts.append(self.GENRE_DESCRIPTORS[genre])

        # Add mood descriptors
        if mood in self.MOOD_DESCRIPTORS:
            parts.append(self.MOOD_DESCRIPTORS[mood])

        # Add YouTube-optimised quality hints
        if use_for_youtube:
            parts.append(
                "professionally mixed, "
                "broadcast quality audio, "
                "clear stereo sound"
            )

        return ", ".join(parts)

    def validate_lyrics(
        self, lyrics: str
    ) -> dict:
        """
        Validates and cleans lyrics for vocal generation.
        """
        if not lyrics or not lyrics.strip():
            return {
                "valid": False,
                "error": "Lyrics cannot be empty"
            }

        if len(lyrics) > 2000:
            return {
                "valid": False,
                "error": (
                    "Lyrics too long. "
                    "Maximum 2000 characters."
                )
            }

        cleaned = lyrics.strip()
        word_count = len(cleaned.split())

        return {
            "valid": True,
            "cleaned_lyrics": cleaned,
            "word_count": word_count,
            "estimated_duration": word_count * 0.5
        }


prompt_processor = PromptProcessor()