from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def escape_md(text):
    if not text:
        return ""
    escape_chars = '_*[]()~`>#+-=|{}.!'
    for ch in escape_chars:
        text = text.replace(ch, '\\' + ch)
    return text

@app.route('/', methods=['POST'])
def webhook():
    if not BOT_TOKEN or not CHAT_ID:
        return "Bot configuration missing", 400

    data = request.get_json(silent=True)
    if not data:
        return "Invalid JSON", 400

    # Ambil semua data yang mungkin dihantar
    signal_type = data.get("type", "Buy").capitalize()
    pair = escape_md(data.get("pair", "Unknown"))
    close = escape_md(data.get("close"))
    sl = escape_md(data.get("sl"))
    tp1 = escape_md(data.get("tp1"))
    tp2 = escape_md(data.get("tp2"))
    tp3 = escape_md(data.get("tp3"))
    risk = escape_md(data.get("risk", "N/A"))
    entry_type = escape_md(data.get("entry_type", "N/A"))

    if not all([close, sl, tp1]):
        return "Missing required data", 400

    # Emoji ikut jenis signal
    if signal_type == "Buy":
        emoji = "🟢"
    elif signal_type == "Sell":
        emoji = "🔴"
    else:
        emoji = "📉"

    # Format mesej dengan emoji
    msg = f"{emoji} *{signal_type} Signal Triggered!*\n"
    msg += f"Pair: {pair}\n"
    msg += f"Entry: {close}\n"
    msg += f"SL: 🛑 {sl}\n"
    msg += f"TP1: 🎯 {tp1}\n"
    if tp2: msg += f"TP2: 🎯 {tp2}\n"
    if tp3: msg += f"TP3: 🎯 {tp3}\n"
    msg += f"Risk: ⚠️ {risk}\n"
    msg += f"Entry Type: {entry_type}"

    # Hantar mesej ke Telegram
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": msg,
                "parse_mode": "Markdown"
            }
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
