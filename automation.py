import os
import subprocess
import webbrowser
import shutil


# =========================
# OPEN APPS (NO HARDCODE)
# =========================
def open_app(app_name: str):
    app_name = app_name.lower()

    # Common Windows apps
    known_apps = {
        "notepad": "notepad",
        "calculator": "calc",
        "cmd": "cmd",
        "paint": "mspaint",
        "explorer": "explorer",
        "chrome": "chrome",
        "edge": "msedge"
    }

    if app_name in known_apps:
        subprocess.Popen(known_apps[app_name])
        return True, f"Opening {app_name}"

    # Try using Windows search (no hardcoding)
    try:
        subprocess.Popen(f'start {app_name}', shell=True)
        return True, f"Opening {app_name}"
    except:
        return False, "App not found"


# =========================
# SYSTEM COMMANDS
# =========================
def shutdown_pc():
    os.system("shutdown /s /t 5")
    return True, "Shutting down the system"


def restart_pc():
    os.system("shutdown /r /t 5")
    return True, "Restarting the system"


# =========================
# AUTOMATION ROUTER
# =========================
def handle_automation(text: str):
    text = text.lower()

    # OPEN APP
    if text.startswith("open "):
        app = text.replace("open ", "").strip()
        return open_app(app)

    # SHUTDOWN
    if "shutdown" in text:
        return shutdown_pc()

    # RESTART
    if "restart" in text:
        return restart_pc()

    # SEARCH (OFFLINE → OPEN BROWSER)
    if text.startswith("search "):
        query = text.replace("search ", "")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return True, f"Searching {query}"

    # NOT AUTOMATION
    return False, None
