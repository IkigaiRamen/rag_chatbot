# src/llm/llm.py
import requests

class LLM:
    def __init__(self, api_url="http://localhost:1234/v1/chat/completions", model_name="mistral-3-3b"):
        self.api_url = api_url
        self.model_name = model_name

    def generate_answer(self, prompt: str, max_tokens: int = 512) -> str:
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }

        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
