import os
import json
import streamlit as st

import config
from utils.llm import kid_safe_reply
from utils.stt import transcribe_bytes
from utils.tts import tts_openai_to_mp3, tts_gtts_multilingual
from utils.translate import translate_with_llm, translate_fallback_googletrans

st.set_page_config(page_title="SpeakGenie", page_icon="🎙️", layout="centered")

# --- Sidebar ---
st.sidebar.title("🎙️ SpeakGenie")
st.sidebar.caption("AI Voice English Tutor (6–16)")
mode = st.sidebar.radio("Mode", ["AI Chatbot", "Roleplay Mode", "Bonus: Native Language Playback"])
st.sidebar.write("---")
st.sidebar.subheader("Config")
st.sidebar.code(f"LLM: {config.LLM_MODEL}\nSTT: {config.STT_MODEL}\nTTS: {config.TTS_MODEL}", language="text")

st.title("🎙️ SpeakGenie — AI Voice English Tutor")

def text_and_voice_reply(reply_text: str, *, english_only=False, regional_lang_code: str | None = None) -> None:
    """Show Genie’s reply in text + play voice."""
    if not reply_text.strip():
        st.warning("No reply text.")
        return
    st.markdown(f"**🤖 Genie:** {reply_text}")

    try:
        if english_only or not regional_lang_code:
            mp3 = tts_openai_to_mp3(reply_text)  # OpenAI TTS for English
        else:
            mp3 = tts_gtts_multilingual(reply_text, regional_lang_code)  # gTTS for regional
        st.audio(mp3)
    except Exception as e:
        st.error(f"TTS error: {e}")

# --- Tutor (AI Chatbot) ---
if mode == "AI Chatbot":
    st.header("👩‍🎓 Talk to Genie")
    st.caption("1) Upload your voice → 2) Transcribe → 3) Genie replies and speaks back")

    # Option 1: Text input
    user_text = st.text_input("Or type your question here:", placeholder="Hi Genie, what is a noun?")

    # Option 2: Upload audio file
    uploaded_file = st.file_uploader("Upload your voice (MP3/WAV):", type=["mp3", "wav"])

    col1, col2 = st.columns(2)
    with col1:
        transcribe_clicked = st.button("📝 Transcribe")
    with col2:
        tutor_clicked = st.button("🧠 Ask Genie")

    # Step 1: STT
    if transcribe_clicked and uploaded_file:
        with st.spinner("Transcribing..."):
            text = transcribe_bytes(uploaded_file.read())
        st.success("Transcription done!")
        st.markdown(f"**🧒 You (STT):** {text}")
        st.session_state["last_transcript"] = text

    # Step 2: LLM reply + TTS
    if tutor_clicked:
        query = user_text.strip() if user_text.strip() else st.session_state.get("last_transcript", "").strip()
        if not query:
            st.warning("Type something or upload and transcribe audio first.")
        else:
            with st.spinner("Genie is thinking..."):
                reply = kid_safe_reply(query)
            text_and_voice_reply(reply, english_only=True)

# --- Roleplay Mode ---
elif mode == "Roleplay Mode":
    st.header("🎭 Practice Real Conversations")
    st.caption("Choose a scenario, then speak OR type. Genie will stay in character and coach you kindly.")

    with open("roleplay/scenarios.json", "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    scenario = st.selectbox("Pick a scenario", list(scenarios.keys()))
    st.write("**Example lines:**")
    for step in scenarios[scenario]:
        st.write(f"🧒 {step['student']}")
        st.write(f"🤖 Genie: {step['genie']}")

    st.write("---")
    st.subheader("🎤 Your Turn")

    # Option 1: Type directly
    user_text = st.text_input("Type your line here:", placeholder="Hello! How are you?")

    # Option 2: Upload audio file
    uploaded_file = st.file_uploader("Upload your roleplay voice (MP3/WAV):", type=["mp3", "wav"], key="roleplay")

    col1, col2, col3 = st.columns(3)
    with col1:
        transcribe_clicked = st.button("📝 Transcribe (Roleplay)")
    with col2:
        coach_clicked = st.button("🎯 Coach Me (from Text)")
    with col3:
        coach_voice_clicked = st.button("🎯 Coach Me (from Recording)")

    # Transcribe uploaded audio
    if transcribe_clicked and uploaded_file:
        with st.spinner("Transcribing..."):
            text = transcribe_bytes(uploaded_file.read())
        st.success("Transcription done!")
        st.markdown(f"**🧒 You (STT):** {text}")
        st.session_state["roleplay_transcript"] = text

    # Coach from text
    if coach_clicked:
        utterance = user_text.strip()
        if utterance:
            with st.spinner("Genie is coaching..."):
                reply = kid_safe_reply(utterance, roleplay_context=scenario)
            text_and_voice_reply(reply, english_only=True)
        else:
            st.warning("Please type something first.")

    # Coach from recorded file
    if coach_voice_clicked:
        utterance = st.session_state.get("roleplay_transcript", "").strip()
        if utterance:
            with st.spinner("Genie is coaching..."):
                reply = kid_safe_reply(utterance, roleplay_context=scenario)
            text_and_voice_reply(reply, english_only=True)
        else:
            st.warning("Please upload + transcribe audio first.")

# --- Bonus: Native Language Playback ---
else:
    st.header("🌐 Native Language Playback (Bonus)")
    st.caption("Translate Genie’s response to a regional language and play audio.")

    user_english = st.text_input("Type Genie’s English reply (or any English text):",
                                 value="A noun is the name of a person, place, or thing.")
    lang_name = st.selectbox("Target Language", list(config.SUPPORTED_REGIONAL_LANGS.keys()))
    lang_code = config.SUPPORTED_REGIONAL_LANGS[lang_name]

    col1, col2 = st.columns(2)
    with col1:
        translate_btn = st.button("🔁 Translate")
    with col2:
        speak_btn = st.button("🔊 Translate + Speak")

    if translate_btn or speak_btn:
        with st.spinner("Translating..."):
            try:
                translated = translate_with_llm(user_english, lang_name)
            except Exception:
                translated = translate_fallback_googletrans(user_english, lang_code)
        st.success("Translated!")
        st.markdown(f"**🌍 {lang_name}:** {translated}")

        if speak_btn:
            with st.spinner("Generating audio..."):
                mp3 = tts_gtts_multilingual(translated, lang_code)
            st.audio(mp3)
