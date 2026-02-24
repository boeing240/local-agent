import requests

OLLAMA_URL = "http://192.168.31.190:11434/api/chat"
MODEL = "qwen2.5:7b-instruct-q4_K_M"


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
