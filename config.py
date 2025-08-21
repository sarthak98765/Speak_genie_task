import os

# Load OPENAI_API_KEY from environment (recommended)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "PASTE YOU API KEY HERE")

# OpenAI models
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")  # chat/text
STT_MODEL = os.getenv("STT_MODEL", "gpt-4o-mini-transcribe")  # fallback to "whisper-1"
TTS_MODEL = os.getenv("TTS_MODEL", "tts-1")  # text-to-speech

# Safety / persona prompt for kids (6-16)
TUTOR_SYSTEM_PROMPT = """
You are Genie, a warm, positive, kid-safe English tutor for ages 6–16.
Speak simply (CEFR A1–B1), be encouraging, and add a friendly emoji occasionally.
Correct gently, avoid adult topics, and never ask for personal data.
Prefer short sentences. Give 1 tip to improve speaking when helpful.
"""

# Languages for bonus playback (ISO codes)
SUPPORTED_REGIONAL_LANGS = {
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Tamil": "ta"
}
