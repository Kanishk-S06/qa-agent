import os
import requests
from dotenv import load_dotenv

# Load .env locally, ignored on Render (Render uses env vars dashboard)
load_dotenv()

# Read API key from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_llm(prompt, model="meta-llama/llama-3.1-8b-instruct"):
    """
    Sends a prompt to OpenRouter's LLM API and returns the response text.

    Works both locally (via .env) and on Render (via dashboard variables).
    """

    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is missing! "
            "Set it in your .env or Render environment variables."
        )

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 900
    }

    response = requests.post(API_URL, headers=headers, json=body)

    # Throw clear, readable error if unauthorized
    if response.status_code == 401:
        raise RuntimeError(
            "❌ Unauthorized: Your OpenRouter API key is invalid or missing."
        )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
