from groq import Groq
from config import GROQ_API_KEY
client = Groq(api_key=GROQ_API_KEY)

def ai_chat(text: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": text}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("AI ERROR:", e)
        return "Sorry sir, I could not process that."
