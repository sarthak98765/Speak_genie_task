import io
import soundfile as sf
import numpy as np
from utils.openai_client import get_client
import config

def _ensure_wav_pcm16(audio_bytes: bytes, sample_rate: int) -> bytes:
    """
    Convert raw float32 PCM buffer to 16-bit WAV in-memory for OpenAI STT.
    Assumes mono float32 array in range [-1, 1].
    """
    data, sr = sf.read(io.BytesIO(audio_bytes), dtype='float32', always_2d=False)
    if isinstance(data, np.ndarray) and data.ndim > 1:
        # Convert to mono
        data = np.mean(data, axis=1)
    if sr != sample_rate:
        # Resample if needed using soundfile? (soundfile doesn't resample)
        # Most WebRTC frames already 32k/48k; OpenAI handles common rates.
        pass
    buf = io.BytesIO()
    sf.write(buf, data, sr, format='WAV', subtype='PCM_16')
    buf.seek(0)
    return buf.read()

def transcribe_bytes(audio_wav_bytes: bytes, file_name: str = "speech.wav") -> str:
    """
    Send WAV bytes to OpenAI transcription. Uses gpt-4o-mini-transcribe when available,
    otherwise falls back to whisper-1.
    """
    client = get_client()
    model = config.STT_MODEL
    try:
        resp = client.audio.transcriptions.create(
            model=model,
            file=("speech.wav", audio_wav_bytes)
        )
        return resp.text.strip()
    except Exception:
        # Fallback to whisper-1
        try:
            resp = client.audio.transcriptions.create(
                model="whisper-1",
                file=("speech.wav", audio_wav_bytes)
            )
            return resp.text.strip()
        except Exception as e:
            return f"[STT error: {e}]"
