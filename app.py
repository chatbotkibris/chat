from flask import Flask, request
import openai
import os

app = Flask(__name__)

# OpenAI API anahtarını ortam değişkeninden al
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    
    # Anahtar kelimeye göre özel yanıt
    if "adım ne" in incoming_msg.lower():
        return respond("Sen Koray'sın :)")

    # OpenAI eski API (Completion) ile cevap üretme
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=incoming_msg,
            max_tokens=200,
            temperature=0.7
        )
        reply = response.choices[0].text.strip()
        return respond(reply)

    except Exception as e:
        return respond(f"Bir hata oluştu: {str(e)}")

def respond(message):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>""", 200, {"Content-Type": "application/xml"}

if __name__ == "__main__":
    app.run()
