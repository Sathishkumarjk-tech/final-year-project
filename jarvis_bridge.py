from intent_classifier import classify_intent
from automation import open_app, search_web, shutdown_pc
from tts import speak
from jarvis_ai import ai_chat


def handle_text(text: str):
    print("🧠 handle_text received:", text)

    if not text or len(text.strip()) < 2:
        print("⚠ Empty or too short text")
        return

    intent = classify_intent(text)
    print("🧭 Intent:", intent)

    if intent == "open_app":
        result = open_app(text.replace("open", "").strip())
        print("⚙ Automation result:", result)
        speak(result)
        return

    if intent == "search":
        result = search_web(text.replace("search", "").strip())
        print("🌐 Search result:", result)
        speak(result)
        return

    if intent == "shutdown":
        result = shutdown_pc()
        print("💻 Shutdown:", result)
        speak(result)
        return

    print("🤖 AI fallback")
    reply = ai_chat(text)
    print("🤖 AI reply:", reply)
    speak(reply)
