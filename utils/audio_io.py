import io
import av
import numpy as np
import soundfile as sf

def frames_to_wav_bytes(frames, sample_rate=48000) -> bytes:
    """
    Collect WebRTC audio frames and convert to WAV bytes (mono PCM16).
    """
    # Concatenate all frames to float32 mono
    audio = np.concatenate([frame.to_ndarray().astype(np.float32) / 32768.0
                            for frame in frames], axis=0)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    buf = io.BytesIO()
    sf.write(buf, audio, sample_rate, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return buf.read()
