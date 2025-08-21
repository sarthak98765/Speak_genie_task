# import tempfile
# from utils.openai_client import get_client
# import config
# from gtts import gTTS

# def tts_openai_to_mp3(text: str) -> str:
#     """
#     English voice via OpenAI TTS (tts-1). Returns path to temp MP3.
#     """
#     client = get_client()
#     out_path = tempfile.mktemp(suffix=".mp3")
#     with open(out_path, "wb") as f:
#         audio = client.audio.speech.create(
#             model=config.TTS_MODEL,       # tts-1
#             voice="alloy",                # built-in voice
#             input=text,
#             format="mp3"
#         )
#         f.write(audio.read())  # SDK streams bytes
#     return out_path

# def tts_gtts_multilingual(text: str, lang_code: str) -> str:
#     """
#     Multilingual fallback using gTTS for regional language playback.
#     """
#     out_path = tempfile.mktemp(suffix=".mp3")
#     tts = gTTS(text=text, lang=lang_code)
#     tts.save(out_path)
#     return out_path
import tempfile
from utils.openai_client import get_client
import config
from gtts import gTTS

def tts_openai_to_mp3(text: str) -> str:
    """
    English voice via OpenAI TTS. Returns path to temp MP3.
    """
    client = get_client()
    out_path = tempfile.mktemp(suffix=".mp3")

    response = client.audio.speech.create(
        model=config.TTS_MODEL,    # e.g. "gpt-4o-mini-tts" or "tts-1"
        voice="alloy",             # available voices: alloy, verse, shimmer
        input=text
    )

    # Save audio to file
    with open(out_path, "wb") as f:
        f.write(response.read())

    return out_path


def tts_gtts_multilingual(text: str, lang_code: str) -> str:
    """
    Multilingual fallback using gTTS for regional language playback.
    """
    out_path = tempfile.mktemp(suffix=".mp3")
    tts = gTTS(text=text, lang=lang_code)
    tts.save(out_path)
    return out_path
