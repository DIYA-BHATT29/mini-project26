import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)

# ---------------------------
# Offline fallback responses
# ---------------------------
def offline_finance_response(message):
    message = message.lower()

    if "mutual fund" in message:
        return "A mutual fund pools money from investors and invests it in stocks, bonds, or other assets."

    elif "sip" in message:
        return "SIP allows you to invest a fixed amount regularly in mutual funds."

    elif "budget" in message:
        return "Budgeting helps track income and expenses to improve savings."

    return "I can help with savings, investments, taxes, loans, and budgeting."

# ---------------------------
# AI Response from OpenRouter
# ---------------------------
def get_ai_response(user_message):

    # If no API key → use offline mode
    if not OPENROUTER_API_KEY:
        return offline_finance_response(user_message)

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "max_tokens": 200,
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": """
You are a smart financial advisor chatbot.

Rules:
- Only answer finance, savings, investment, tax, loan, or money related questions.
- If question is unrelated, politely refuse.
- Keep answers short and beginner friendly.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]

        else:
            print("API ERROR:", response.text)
            return offline_finance_response(user_message)

    except Exception as e:
        print("EXCEPTION:", e)
        return offline_finance_response(user_message)

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Please ask a valid finance question."})

    bot_reply = get_ai_response(user_message)

    return jsonify({"response": bot_reply})

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    print("Smart Financial Advisor Started")
    app.run(debug=True)
