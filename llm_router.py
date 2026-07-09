from net import internet_available
from groq import Groq
from config import GROQ_API_KEY
import subprocess

# ---------- ONLINE (Groq) ----------
groq_client = Groq(api_key=GROQ_API_KEY)

def online_llm(prompt):
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


# ---------- LOCAL (Ollama) ----------
def local_llm(prompt: str):
    # Clean input for Windows console
    safe_prompt = prompt.encode("utf-8", errors="ignore").decode("utf-8")

    result = subprocess.run(
        ["ollama", "run", "phi3"],
        input=safe_prompt,
        text=True,
        encoding="utf-8",
        capture_output=True
    )

    return result.stdout.strip()



# ---------- ROUTER ----------
def ask_llm(prompt):
    if internet_available():
        try:
            return online_llm(prompt)
        except:
            return local_llm(prompt)
    else:
        return local_llm(prompt)
