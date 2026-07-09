import time
import json
import psutil
import datetime
import socket
import threading


from tts import speak
from groq import Groq
from config import GROQ_API_KEY

# ===================== CONFIG =====================

MEMORY_FILE = "jarvis_memory.json"
INTERRUPT_COOLDOWN = 600  # seconds
TRAY_TOOLTIP = "Jarvis Active"

client = Groq(api_key=GROQ_API_KEY)

# ===================== MEMORY =====================

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "sleep_times": [],
            "interrupts": 0,
            "last_interrupt": 0,
            "user_mood": "neutral"
        }

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

memory = load_memory()

# ===================== UTILITIES =====================

def internet_available():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

def get_time():
    return datetime.datetime.now()

# ===================== EMOTION ENGINE =====================

def detect_emotion(text):
    text = text.lower()
    if any(w in text for w in ["tired", "sad", "angry", "frustrated"]):
        return "negative"
    if any(w in text for w in ["happy", "great", "awesome", "good"]):
        return "positive"
    return "neutral"

# ===================== AI INTERRUPT DECISION =====================

def should_interrupt(context):
    now = time.time()

    if now - memory["last_interrupt"] < INTERRUPT_COOLDOWN:
        return False

    try:
        decision = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"""
Should I interrupt the user now?

Context:
{context}

Reply only YES or NO.
"""
            }]
        ).choices[0].message.content.strip().upper()

        if decision == "YES":
            memory["last_interrupt"] = now
            memory["interrupts"] += 1
            save_memory(memory)
            return True

    except:
        pass

    return False

# ===================== PROACTIVE RULES =====================

def night_routine():
    hour = get_time().hour
    if hour >= 23:
        memory["sleep_times"].append(hour)
        save_memory(memory)
        return "It's getting late. You usually stay up late. Should I remind you to rest?"

def battery_check():
    bat = psutil.sensors_battery()
    if bat and bat.percent <= 20 and not bat.power_plugged:
        return f"Battery is at {bat.percent} percent. I recommend charging."

def cpu_check():
    if psutil.cpu_percent(interval=1) > 85:
        return "System is under heavy load. I can optimize performance."

def emotion_based_suggestion():
    if memory["user_mood"] == "negative":
        return "You seem stressed lately. Would you like a break or some music?"

# ===================== PROACTIVE LOOP =====================

def proactive_loop():
    speak("Proactive intelligence online.")

    while True:
        suggestions = [
            night_routine(),
            battery_check(),
            cpu_check(),
            emotion_based_suggestion()
        ]

        for s in suggestions:
            if s and should_interrupt(s):
                speak(s)

        time.sleep(300)

# ===================== SYSTEM TRAY =====================

def create_icon():
    img = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(img)
    draw.text((18, 18), "J", fill="cyan")
    return img

def tray_quit(icon, item):
    speak("Shutting down Jarvis.")
    icon.stop()
    exit(0)

def tray_thread():
    menu = pystray.Menu(
        pystray.MenuItem("Exit Jarvis", tray_quit)
    )
    icon = pystray.Icon("Jarvis", create_icon(), TRAY_TOOLTIP, menu)
    icon.run()

# ===================== START FUNCTION =====================

def start_proactive_system():
    threading.Thread(target=proactive_loop, daemon=True).start()
    threading.Thread(target=tray_thread, daemon=True).start()
