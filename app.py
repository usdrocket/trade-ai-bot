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

    # Dapatkan semua nilai dengan default kosong jika tiada
    signal_type = data.get("type", "").upper()
    pair = data.get("pair", "Unknown")
    close = data.get("close", "-")
    sl = data.get("sl", "-")
    tp1 = data.get("tp1", "-")
    tp2 = data.get("tp2", "-")
    tp3 = data.get("tp3", "-")
    risk = data.get("risk", "-")
    entry_type = data.get("entry_type", "-")

    # Format mesej
    msg = (
        f"📡 *{signal_type} SIGNAL*\n"
        f"📊 Pair: {pair}\n"
        f"🎯 Entry: {close} ({entry_type})\n"
        f"🛑 SL: {sl}\n"
        f"✅ TP1: {tp1}\n"
        f"✅ TP2: {tp2}\n"
        f"✅ TP3: {tp3}\n"
        f"⚠️ Risk Level: {risk}"
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
    app.run(host='0.0.0.0', port=8080)
