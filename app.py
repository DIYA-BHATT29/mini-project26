import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found. Check your .env file.")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Finance keyword filter
FINANCE_KEYWORDS = [
    "money", "finance", "investment", "invest", "stock",
    "mutual fund", "saving", "savings", "budget",
    "bank", "loan", "credit", "debit",
    "tax", "insurance", "retirement",
    "crypto", "bitcoin", "wealth",
    "income", "expense", "portfolio",
    "sip", "ppf", "epf", "gst"
]

def is_finance_related(question):
    question = question.lower()
    return any(keyword in question for keyword in FINANCE_KEYWORDS)


def get_financial_response(user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional financial advisor chatbot. "
                    "Only answer questions related to finance, money, "
                    "investments, savings, taxes, insurance, banking, "
                    "wealth management, and budgeting. "
                    "If the question is unrelated, politely refuse."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.5
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        return "⚠️ Unable to connect to financial advisor service."

    result = response.json()

    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return "⚠️ Unexpected response format from API."


# Homepage
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"reply": "⚠️ Invalid request."})

    user_message = data["message"].strip()

    if not user_message:
        return jsonify({"reply": "⚠️ Please enter a message."})

    # Restrict to finance-related queries
    if not is_finance_related(user_message):
        return jsonify({
            "reply": "❌ I only provide advice on finance, money, savings, investments, taxes, and related topics."
        })

    bot_reply = get_financial_response(user_message)

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
