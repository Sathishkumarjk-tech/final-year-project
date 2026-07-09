import threading
import time

from stt_realtime import listen
from tts import speak
from wakeword.wake_word import wait_for_wake_word
from automation import handle_automation
from llm_router import ask_llm
from net_utils import has_internet

# Telegram is OPTIONAL
try:
    from telegram_bot import run_bot
    TELEGRAM_AVAILABLE = True
except:
    TELEGRAM_AVAILABLE = False


# ===============================
# START TELEGRAM (ONLY ONLINE)
# ===============================
def start_telegram():
    if not TELEGRAM_AVAILABLE:
        print("📴 Telegram module missing")
        return

    if not has_internet():          
        print("📴 Telegram disabled (no internet)")
        return

    def _run():
        try:
            run_bot()
        except Exception as e:
            print("⚠ Telegram stopped:", e)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    print("📱 Telegram bot running")


# ===============================
# MAIN VOICE LOOP
# ===============================
def voice_loop():
    while True:
        print("💤 Waiting for wake word: Jarvis")
        wait_for_wake_word()

        print("⚡ Wake word detected")
        speak("Yes sir")

        print("🎤 Listening...")
        text = listen()

        if not text:
            speak("I did not hear anything")
            continue

        print("🗣 You said:", text)

        # 1️⃣ AUTOMATION (OFFLINE)
        handled, reply = handle_automation(text)
        if handled:
            speak(reply)
            continue

        # 2️⃣ AI RESPONSE (AUTO LOCAL / ONLINE)
        try:
            response = ask_llm(text)
        except Exception as e:
            print("LLM ERROR:", e)
            response = "Something went wrong"

        speak(response)


# ===============================
# START JARVIS
# ===============================
def start_jarvis():
    speak("Jarvis online")

    # Telegram only if internet exists
    start_telegram()

    # Voice assistant always works
    voice_loop()


# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    start_jarvis()
