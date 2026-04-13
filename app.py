from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def summarize_text(message: str, tone: str) -> str:
    if not OPENROUTER_API_KEY:
        return "⚠️ API key not found. Please set OPENROUTER_API_KEY in your .env file."
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"Summarize the following message into 3 bullet points using a {tone} tone:\n\n{message}"
    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )
        data = response.json()
        if response.status_code == 200 and "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            error_msg = data.get("error", {}).get("message") or data.get("detail") or str(data)
            return f"⚠️ API Error: {error_msg}"
    except requests.RequestException as error:
        print("Error:", error)
        return "⚠️ Unable to summarize. Network or API error."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    message = request.form.get("message", "")
    tone = request.form.get("tone", "professional")
    if not message.strip():
        return jsonify({"summary": "⚠️ Message input is empty. Please enter some content."})
    summary = summarize_text(message, tone)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
