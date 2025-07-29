from flask import Flask, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    
    # Basit karşılama veya kişisel cevap örneği
    if "adım ne" in incoming_msg.lower():
        return respond("Sen Koray'sın :)")

    # ChatGPT ile cevaplama
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": incoming_msg}]
    )

    reply = response.choices[0].message["content"]
    return respond(reply)

def respond(message):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>""", 200, {"Content-Type": "application/xml"}

if __name__ == "__main__":
    app.run()
