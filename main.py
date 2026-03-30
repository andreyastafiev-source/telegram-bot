from flask import Flask, request
import requests
import json
import os

TOKEN = os.environ.get("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)


def send_text(chat_id, text):
    requests.post(URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })


def send_buttons(chat_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "🧠 Анализ состояния", "web_app": {"url": "https://andreyastafiev-source.github.io/hypnosis-webapp/?mode=diagnostic"}}],
            [{"text": "🎧 Снижение тревоги", "web_app": {"url": "https://andreyastafiev-source.github.io/hypnosis-webapp/?mode=audio"}}],
            [{"text": "⚡ Разбор ситуации", "web_app": {"url": "https://andreyastafiev-source.github.io/hypnosis-webapp/?mode=fast"}}],
            [{"text": "👨‍⚕️ Супервизия", "web_app": {"url": "https://andreyastafiev-source.github.io/hypnosis-webapp/?mode=supervision"}}]
        ]
    }

    requests.post(URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": "Выберите, с чем хотите поработать 👇",
        "reply_markup": keyboard
    })


@app.route("/", methods=["GET"])
def home():
    return "Bot is running"


@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("UPDATE:", data)

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]

        if "web_app_data" in message:
            raw = message["web_app_data"]["data"]

            try:
                parsed = json.loads(raw)
            except:
                parsed = {"raw": raw}

            if parsed.get("type") == "diagnostic":
                send_text(chat_id, f"🧠 Результат: {parsed.get('score')} баллов")

            elif parsed.get("type") == "audio":
                send_text(chat_id, "🎧 Хочет консультацию")

            elif parsed.get("type") == "fast":
                send_text(chat_id, f"⚡ Разбор:\n{parsed.get('data')}")

            elif parsed.get("type") == "supervision":
                send_text(chat_id, f"👨‍⚕️ Супервизия:\n{parsed.get('data')}")

            return "ok"

        send_buttons(chat_id)

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
