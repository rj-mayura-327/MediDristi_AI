import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Fix OMP duplicate DLL in Anaconda

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

GROK_MODEL = "llama-3.3-70b-versatile"  # Groq model
GROK_BASE_URL = "https://api.groq.com/openai/v1"  # Groq base URL

_PLACEHOLDERS = {
    "", "your_xai_api_key_here",
    "xai-put-your-real-key-here",
    "PASTE_YOUR_REAL_XAI_KEY_HERE",
}


def get_llm(temperature: float = 0.3) -> ChatOpenAI:
    api_key = os.getenv("XAI_API_KEY", "").strip()
    if api_key in _PLACEHOLDERS:
        raise ValueError(
            "XAI_API_KEY not found. "
            "Add your real xAI API key to the .env file.\n"
            "Get your key at: https://console.x.ai/"
        )
    return ChatOpenAI(
        model=GROK_MODEL,
        api_key=api_key,
        base_url=GROK_BASE_URL,
        temperature=temperature,
    )
