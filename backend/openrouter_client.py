import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

API_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_llm(prompt, model="meta-llama/llama-3.1-8b-instruct"):
    """
    Sends a prompt to OpenRouter LLM API and returns the response text.
    Free tier supported.
    """
    body = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 800
    }

    response = requests.post(API_URL, headers=HEADERS, json=body)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
