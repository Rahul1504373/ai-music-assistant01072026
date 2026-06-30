import streamlit as st
import requests
import os
import json
from src.config import FASTAPI_URL, GENRES, MOODS, DURATIONS

st.set_page_config(
    page_title="AI Music Assistant",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -- Custom CSS (Suno-like Dark Theme) --------------------------
st.markdown("""
<style>
    .main { background-color: #0a0a0a; color: #ffffff; }
    .stApp { background-color: #0a0a0a; }
    .music-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #0f3460;
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
    }
    .license-badge {
        background: #1a2a1a;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 8px 16px;
        color: #4caf50;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# -- Header -------------------------------------------------------
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(
        "<h1 style='text-align:center; "
        "background: linear-gradient(135deg, #667eea, #764ba2);"
        "-webkit-background-clip: text;"
        "-webkit-text-fill-color: transparent;"
        "font-size: 3em;'>🎵 AI Music Assistant</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#888; "
        "font-size:1.1em;'>"
        "Generate 100% original, copyright-free music "
        "for YouTube & Instagram</p>",
        unsafe_allow_html=True
    )

st.divider()

# -- Main Layout ----------------------------------------------------
left_col, right_col = st.columns([3, 2])

with left_col:
    tab1, tab2 = st.tabs([
        "🎵 Create Music",
        "🎨 Style from Reference"
    ])

    # ============================================================
    # TAB 1: Create Original Music
    # ============================================================
    with tab1:
        st.markdown("### 🎼 Describe Your Music")

        prompt = st.text_area(
            "Music Prompt",
            placeholder=(
                "E.g., 'A cinematic orchestral piece with "
                "rising strings and powerful drums, "
                "perfect for a hero's journey...'"
            ),
            height=100,
            key="main_prompt"
        )

        col_g, col_m = st.columns(2)
        with col_g:
            genre = st.selectbox("🎸 Genre", GENRES, index=0)
        with col_m:
            mood = st.selectbox("😊 Mood", MOODS, index=0)

        col_t, col_d = st.columns(2)
        with col_t:
            tempo = st.select_slider(
                "⚡ Tempo",
                options=["slow", "medium", "fast", "very_fast"],
                value="medium"
            )
        with col_d:
            duration = st.select_slider(
                "⏱️ Duration (seconds)",
                options=DURATIONS,
                value=30
            )

        st.markdown("#### 🎹 Select Instruments")
        instrument_options = [
            "piano", "guitar", "drums", "bass",
            "violin", "saxophone", "synthesizer",
            "flute", "cello", "trumpet",
            "acoustic guitar", "electric guitar"
        ]
        instruments = st.multiselect(
            "Instruments (optional)",
            instrument_options,
            default=["piano", "drums"]
        )

        st.divider()

        st.markdown("### 🎤 Vocals (Optional)")
        include_vocals = st.toggle(
            "Add AI Vocals",
            value=False,
            help="Add synthetic AI vocals to your music"
        )

        if include_vocals:
            lyrics = st.text_area(
                "Lyrics",
                placeholder=(
                    "Enter your song lyrics here...\n\n"
                    "[Verse 1]\n"
                    "Your lyrics here...\n\n"
                    "[Chorus]\n"
                    "Your chorus here..."
                ),
                height=200
            )

            voice_options = {
                "female_1": "Female Voice 1 (Bright)",
                "female_2": "Female Voice 2 (Warm)",
                "female_3": "Female Voice 3 (Deep)",
                "female_4": "Female Voice 4 (Clear)",
                "female_5": "Female Voice 5 (Soft)",
                "male_1":   "Male Voice 1 (Deep)",
                "male_2":   "Male Voice 2 (Warm)",
                "male_3":   "Male Voice 3 (Clear)",
                "male_4":   "Male Voice 4 (Bright)",
                "male_5":   "Male Voice 5 (Powerful)",
            }

            voice_preset = st.selectbox(
                "🎤 AI Voice (100% Synthetic)",
                options=list(voice_options.keys()),
                format_func=lambda x: voice_options[x]
            )

            st.info(
                "All voices are 100% synthetic AI voices. "
                "No real person's voice is used or cloned."
            )
        else:
            lyrics = ""
            voice_preset = "female_1"

        st.divider()

        st.markdown("### 📱 Platform Settings")
        col_yt, col_ig = st.columns(2)
        with col_yt:
            for_youtube = st.checkbox(
                "🎬 Optimise for YouTube", value=True
            )
        with col_ig:
            for_instagram = st.checkbox(
                "📱 Optimise for Instagram", value=True
            )

        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button(
            "🎵 Generate Music",
            type="primary",
            use_container_width=True
        )

        if generate_btn:
            if not prompt.strip():
                st.error("Please enter a music description!")
            else:
                with st.spinner(
                    "🎵 Composing your music... "
                    "This may take 5-15 minutes on CPU..."
                ):
                    try:
                        payload = {
                            "prompt": prompt,
                            "lyrics": lyrics,
                            "genre": genre,
                            "mood": mood,
                            "tempo": tempo,
                            "duration": duration,
                            "instruments": instruments,
                            "voice_preset": voice_preset,
                            "include_vocals": (
                                include_vocals
                                and bool(lyrics.strip())
                            ),
                            "use_for_youtube": (
                                for_youtube or for_instagram
                            )
                        }

                        response = requests.post(
                            f"{FASTAPI_URL}/generate",
                            json=payload,
                            timeout=900
                        )
                        result = response.json()

                        if result.get("status") == "success":
                            st.session_state["last_result"] = result
                            st.success("✅ Music generated successfully!")
                        else:
                            st.error(
                                f"Error: "
                                f"{result.get('error', 'Unknown error')}"
                            )

                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")

    # ============================================================
    # TAB 2: Style from Reference
    # ============================================================
    with tab2:
        st.markdown("### 🎨 Generate in Similar Style")
        st.info(
            "Upload a reference song to extract its musical "
            "style (tempo, key, energy). Our AI will create "
            "completely new original music inspired by that "
            "style — no audio is copied or sampled."
        )

        ref_file = st.file_uploader(
            "Upload Reference Audio",
            type=["mp3", "wav", "flac", "ogg", "m4a"]
        )

        style_prompt = st.text_area(
            "Your Music Description",
            placeholder=(
                "E.g., 'Upbeat summer vibes with catchy melody...'"
            ),
            height=80
        )

        style_duration = st.select_slider(
            "Duration",
            options=DURATIONS,
            value=30,
            key="style_duration"
        )

        analyze_btn = st.button(
            "🔍 Analyse Style & Generate",
            type="primary",
            use_container_width=True,
            key="analyze_btn"
        )

        if analyze_btn and ref_file:
            with st.spinner("Analysing musical style..."):
                try:
                    analyze_response = requests.post(
                        f"{FASTAPI_URL}/analyze-style",
                        files={"file": (
                            ref_file.name,
                            ref_file.getvalue(),
                            ref_file.type
                        )},
                        timeout=60
                    )
                    analyze_result = analyze_response.json()

                    if analyze_result.get("status") == "success":
                        features = analyze_result["features"]
                        st.success("✅ Style analysed!")

                        with st.expander("📊 Extracted Style Features"):
                            col_f1, col_f2 = st.columns(2)
                            with col_f1:
                                st.metric(
                                    "Tempo",
                                    f"{features.get('tempo_bpm', 0):.0f} BPM"
                                )
                                st.metric("Key", features.get("key", "C"))
                                st.metric(
                                    "Genre",
                                    features.get("estimated_genre", "Pop")
                                )
                            with col_f2:
                                st.metric(
                                    "Mood",
                                    features.get("estimated_mood", "Happy")
                                )
                                st.metric(
                                    "Energy",
                                    features.get(
                                        "energy_category", "medium"
                                    ).upper()
                                )
                                st.metric(
                                    "Suggested Instruments",
                                    ", ".join(
                                        features.get("instruments", [])[:3]
                                    )
                                )

                        with st.spinner("Generating inspired music..."):
                            gen_response = requests.post(
                                f"{FASTAPI_URL}/generate-with-style",
                                json={
                                    "prompt": style_prompt,
                                    "reference_features": features,
                                    "duration": style_duration,
                                    "include_vocals": False,
                                    "lyrics": "",
                                    "voice_preset": "female_1"
                                },
                                timeout=900
                            )
                            gen_result = gen_response.json()

                            if gen_result.get("status") == "success":
                                st.session_state["last_result"] = gen_result
                                st.success(
                                    "✅ Style-inspired music generated!"
                                )
                                st.info(gen_result.get("legal_note", ""))

                except Exception as e:
                    st.error(f"Error: {str(e)}")

# -- Right Column: Music Player & Results --------------------------
with right_col:
    st.markdown("### 🎧 Generated Music")

    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        filename = result.get("final_filename", "")

        if filename:
            try:
                audio_response = requests.get(
                    f"{FASTAPI_URL}/download/{filename}",
                    timeout=30
                )

                if audio_response.status_code == 200:
                    st.audio(audio_response.content, format="audio/wav")

                    st.download_button(
                        label="⬇️ Download Music",
                        data=audio_response.content,
                        file_name=filename,
                        mime="audio/wav",
                        use_container_width=True
                    )

                    metadata = result.get("metadata", {})
                    if metadata:
                        with st.expander("📋 Track Details"):
                            st.write(f"**Genre:** {metadata.get('genre', 'N/A')}")
                            st.write(f"**Mood:** {metadata.get('mood', 'N/A')}")
                            st.write(f"**Duration:** {metadata.get('duration', 0)}s")
                            st.write(
                                f"**Has Vocals:** "
                                f"{'Yes' if metadata.get('has_vocals') else 'No'}"
                            )

                    st.markdown("""
                    <div class="license-badge">
                    ✅ AI-Generated Music<br>
                    ✅ No human authorship<br>
                    ✅ Verify model license before publishing<br>
                    ✅ Check YouTube/Instagram policies
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Could not load audio: {str(e)}")

    else:
        st.markdown("""
        <div style='text-align:center; color:#555; padding:60px 20px;
                    border: 2px dashed #333; border-radius:16px;'>
            <h2>🎵</h2>
            <p>Your generated music will appear here</p>
            <p style='font-size:12px;'>
            Create your first track using the form on the left
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    with st.expander("⚖️ Copyright & Legal Information"):
        st.markdown("""
        **About AI-Generated Music & Copyright:**

        - AI-generated music has **no human author**
        - Always verify the **model's license** before commercial use
        - MusicGen: facebook/musicgen-small — check license terms
        - Bark vocals: MIT license (commercial OK)

        **Style Reference Feature:**
        - Only extracts abstract features (tempo, key, energy)
        - No audio from reference is copied or sampled
        - Output is 100% new original composition
        """)