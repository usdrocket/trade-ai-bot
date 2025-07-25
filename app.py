from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/', methods=['POST'])
def webhook():
    if not BOT_TOKEN or not CHAT_ID:
        return "Bot configuration missing", 400

    data = request.get_json(silent=True)
    if not data:
        return "Invalid JSON", 400

    signal_type = data.get("type", "Buy").capitalize()  # Default = Buy
    close = data.get("close")
    sl = data.get("sl")
    tp1 = data.get("tp1")
    pair = data.get("pair", "Unknown Pair")
    risk = data.get("risk", "Not Set")
    entry_type = data.get("entry_type", "N/A")

    if not all([close, sl, tp1]):
        return "Missing required data", 400

    emoji = "📈" if signal_type == "Buy" else "📉"
    msg = (
        f"{emoji} *{signal_type} Signal Triggered!*\n"
        f"Pair: {pair}\n"
        f"Entry: {close}\nSL: {sl}\nTP1: {tp1}\n"
        f"Type: {entry_type}\nRisk: {risk}"
    )

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Failed to send message: {str(e)}", 500

    return "OK", 200

@app.route('/')
def index():
    return "Bot is running", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
