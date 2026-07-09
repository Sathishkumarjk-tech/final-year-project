def classify_intent(text: str):
    text = text.lower()

    if text.startswith("open "):
        return "open_app"

    if text.startswith("search ") or "google" in text:
        return "search"

    if "shutdown" in text or "turn off pc" in text:
        return "shutdown"

    return "chat"
