# Author: ChatGPT
import openai

from app.config import LLM_ENDPOINT, LLM_MODEL

openai.api_base = LLM_ENDPOINT
openai.api_key = "ollama"


def query_llm(prompt):
    response = openai.ChatCompletion.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response["choices"][0]["message"]["content"]
