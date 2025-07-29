from flask import Flask, request
from openai import OpenAI
import os
from reminders import add_reminder, list_reminders_for_user, get_due_reminders
from datetime import datetime
import dateparser
from twilio.rest import Client

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Twilio ayarları
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_PHONE")  # örn: "whatsapp:+14155238886"
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    if "adım ne" in incoming_msg.lower():
        return respond("Sen Koray'sın :)")

    if "listele" in incoming_msg.lower():
        return respond(list_reminders_for_user(sender))

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = response.choices[0].message.content.strip()

        dt = dateparser.parse(incoming_msg, languages=["tr"])
        if dt and dt > datetime.now():
            add_reminder(
                phone_number=sender,
                time_str=dt.isoformat(),
                message=f"{dt.strftime('%d %B %Y %H:%M')} için hatırlatma",
                original_text=incoming_msg
            )
            reply += f"\n✅ Hatırlatıcı kuruldu: {dt.strftime('%d %B %Y %H:%M')}"

        return respond(reply)

    except Exception as e:
        return respond(f"Bir hata oluştu:\n{str(e)}")

@app.route("/check", methods=["GET"])
def check_reminders():
    due = get_due_reminders()
    for r in due:
        twilio_client.messages.create(
            body=f"🔔 Hatırlatma: {r['message']}",
            from_=TWILIO_FROM,
            to=r["phone"]
        )
    return "Kontrol tamamlandı", 200

def respond(message):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>""", 200, {"Content-Type": "application/xml"}

if __name__ == "__main__":
    app.run()
