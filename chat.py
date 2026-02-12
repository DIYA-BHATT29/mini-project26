import os
import requests
import json

# 🔐 Set your OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("⚠️ Please set your OPENROUTER_API_KEY as an environment variable.")
    exit()

# 🌍 OpenRouter endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# 💰 Finance Keywords Filter
FINANCE_KEYWORDS = [
    "money", "finance", "investment", "invest", "stock", "mutual fund",
    "saving", "savings", "budget", "bank", "loan", "credit", "debit",
    "tax", "insurance", "retirement", "crypto", "bitcoin",
    "wealth", "income", "expense", "financial", "portfolio"
]

def is_finance_related(question):
    question = question.lower()
    return any(keyword in question for keyword in FINANCE_KEYWORDS)


def ask_openrouter(question):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",  # You can change model if needed
        "messages": [
            {
                "role": "system",
                "content": "You are a smart financial advisor chatbot. Only answer questions related to money, finance, savings, investments, budgeting, taxes, insurance, banking, or wealth building. If the question is unrelated, politely refuse."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return "⚠️ Error: Unable to fetch response."


def main():
    print("💰 Smart Financial Advisor Chatbot")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot: Stay financially smart! 👋")
            break

        if not is_finance_related(user_input):
            print("Chatbot: ❌ I only answer finance-related questions (money, savings, investments, taxes, etc).")
            continue

        reply = ask_openrouter(user_input)
        print("Chatbot:", reply)
        print()


if __name__ == "__main__":
    main()
