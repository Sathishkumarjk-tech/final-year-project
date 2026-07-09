import sounddevice as sd
import numpy as np
import queue
import torch
import whisper
import time

# ---------------- CONFIG ----------------

SAMPLE_RATE = 16000
MAX_RECORD_SECONDS = 8
SILENCE_TIMEOUT = 1.2   # seconds of silence to stop recording

# ---------------- LOAD MODELS ----------------

print("🔄 Loading Whisper model...")
whisper_model = whisper.load_model("base")   # offline
print("✅ Whisper loaded")

print("🔄 Loading Silero VAD...")
vad_model, vad_utils = torch.hub.load(
    repo_or_dir="snakers4/silero-vad",
    model="silero_vad",
    trust_repo=True
)
(get_speech_timestamps,
 save_audio,
 read_audio,
 VADIterator,
 collect_chunks) = vad_utils
print("✅ VAD loaded")

# ---------------- AUDIO BUFFER ----------------

audio_queue = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

# ---------------- TEXT FILTER ----------------

def is_valid_text(text: str) -> bool:
    if not text:
        return False
    if len(text) < 3:
        return False

    # Reject garbage unicode
    non_ascii_ratio = sum(1 for c in text if ord(c) > 127) / len(text)
    return non_ascii_ratio < 0.3

# ---------------- MAIN LISTEN FUNCTION ----------------

def listen():
    print("🎤 Listening...")

    audio_data = []
    silence_start = None
    speech_detected = False

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        dtype="float32"
    ):
        start_time = time.time()

        while True:
            if time.time() - start_time > MAX_RECORD_SECONDS:
                break

            try:
                chunk = audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            audio_data.append(chunk)

            audio_np = np.concatenate(audio_data, axis=0).flatten()
            audio_tensor = torch.from_numpy(audio_np)

            speech_timestamps = get_speech_timestamps(
                audio_tensor,
                vad_model,
                sampling_rate=SAMPLE_RATE
            )

            if speech_timestamps:
                if not speech_detected:
                    print("✔ Speech detected")
                speech_detected = True
                silence_start = None
            else:
                if speech_detected:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > SILENCE_TIMEOUT:
                        break

    if not audio_data:
        return None

    audio_np = np.concatenate(audio_data, axis=0).flatten()

    # ---------------- WHISPER TRANSCRIBE ----------------

    result = whisper_model.transcribe(
        audio_np,
        language="en",
        temperature=0.0,
        fp16=False
    )

    text = result.get("text", "").strip()

    if not is_valid_text(text):
        print("⚠ Ignoring noisy / invalid speech")
        return None

    print(f"🗣️ You said: {text}")
    return text
