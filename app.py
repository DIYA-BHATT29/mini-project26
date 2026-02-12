import requests

def get_financial_response(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Smart Financial Advisor"
    }

    data = {
    "model": "openai/gpt-3.5-turbo",
    "max_tokens": 300,
    "temperature": 0.7,
    "messages": [
        {
            "role": "system",
            "content": """
You are a smart financial advisor chatbot.

Rules:
- Only answer finance-related questions.
- Refuse unrelated questions.
- Keep answers short and beginner-friendly (6-8 lines max).
"""
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
}


    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Error:", response.text)
        return "⚠ Financial advisor service is currently unavailable."


