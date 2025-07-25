from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    if not data:
        return "Invalid JSON", 400
    
    close = data.get("close")
    sl = data.get("sl")
    tp1 = data.get("tp1")
    
    if not all([close, sl, tp1]):
        return "Missing required data", 400
    
    msg = f"📈 *Buy Signal Triggered!*\nEntry: {close}\nSL: {sl}\nTP1: {tp1}"
    
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
