from flask import Flask, request
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    if "adım ne" in incoming_msg.lower():
        return respond("Sen Koray'sın :)")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ya da "gpt-4"
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = response.choices[0].message.content.strip()
        return respond(reply)

    except Exception as e:
        return respond(f"Bir hata oluştu:\n{str(e)}")

def respond(message):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>""", 200, {"Content-Type": "application/xml"}

if __name__ == "__main__":
    app.run()
