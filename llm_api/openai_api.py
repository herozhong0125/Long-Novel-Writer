from typing import Optional
from openai import OpenAI


client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key="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"
)

def call_openai_api(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 1000) -> str:
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1
            )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"调用 OpenAI API 时发生错误: {e}")
        return ""