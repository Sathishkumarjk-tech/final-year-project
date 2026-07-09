import requests
import socket
from groq import Groq
from config import GROQ_API_KEY

# ---------- ONLINE AI (Groq) ----------
groq_client = Groq(api_key=GROQ_API_KEY)


def internet_available():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        return False


def ai_online(text):
    try:
        resp = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": text}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        print("Online AI error:", e)
        return None


# ---------- OFFLINE AI (Ollama) ----------
def ai_offline(text):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": text,
                "stream": False
            },
            timeout=10
        )
        return r.json()["response"]
    except Exception as e:
        print("Offline AI error:", e)
        return None


# ---------- HYBRID DECIDER ----------
def ai_chat(text):
    if internet_available():
        reply = ai_online(text)
        if reply:
            return reply

    reply = ai_offline(text)
    if reply:
        return reply

    return "Sorry sir, I am offline and unable to process that request."
