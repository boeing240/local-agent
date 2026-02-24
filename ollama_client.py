import requests
from config import OLLAMA_URL, MODEL


class OllamaClient:
    def chat(self, messages: list, tools: list) -> dict:
        payload = {
            "model": MODEL,
            "messages": messages,
            "tools": tools,
            "stream": False,
        }
        resp = requests.post(OLLAMA_URL, json=payload, timeout=30000)
        if not resp.ok:
            print(f"Ollama error {resp.status_code}: {resp.text}")
        resp.raise_for_status()
        data = resp.json()
        return data["message"]
