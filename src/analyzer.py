import os
import time
from google import genai
from dotenv import load_dotenv
from src.prompts import SYSTEM_PROMPT, build_user_prompt

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SKIP = ("image", "tts", "live", "audio", "embedding", "robotics")


def get_models():
    """Ask Google which flash models your key can use, lite ones first."""
    names = []
    for m in client.models.list():
        name = m.name.replace("models/", "")
        if "flash" in name and not any(s in name for s in SKIP):
            names.append(name)
    names.sort(key=lambda n: ("lite" not in n, n))
    return names


def analyze_code(code: str, language: str = "Python") -> str:
    prompt = SYSTEM_PROMPT + "\n\n" + build_user_prompt(code, language)
    last_error = None

    for model in get_models()[:5]:
        for attempt in range(2):
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                return response.text
            except Exception as e:
                last_error = e
                msg = str(e)
                if "503" in msg or "429" in msg or "UNAVAILABLE" in msg:
                    time.sleep(2)
                    continue
                break  # model not found or other problem: try the next model

    raise last_error or Exception("No Gemini models available for this key.")