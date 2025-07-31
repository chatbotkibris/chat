from flask import Flask, request
from openai import OpenAI
from datetime import datetime, timezone
import os
import dateparser
from reminders import add_reminder, list_reminders_for_user, get_due_reminders
from memory import save_message, get_conversation
from twilio.rest import Client

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_PHONE")
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    if "adım ne" in incoming_msg.lower():
        return respond("Sen Koray'sın :)")

    if "listele" in incoming_msg.lower():
        return respond(list_reminders_for_user(sender))

    # Tarih varsa hatırlatıcı kur
    dt = dateparser.parse(
        incoming_msg,
        settings={'TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True},
        languages=["tr"]
    )

    if dt and dt > datetime.now(timezone.utc):
        readable_time = dt.astimezone().strftime('%d %B %Y %H:%M')
        add_reminder(
            phone_number=sender,
            time_str=dt.isoformat(),
            message=f"{readable_time} için hatırlatma",
            original_text=incoming_msg
        )
        return respond(f"✅ Hatırlatıcı kuruldu: {readable_time}")

    # 🧠 Hafızalı GPT cevabı
    try:
        conversation = get_conversation(sender)
        conversation.append({"role": "user", "content": incoming_msg})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation
        )
        reply = response.choices[0].message.content.strip()

        save_message(sender, "user", incoming_msg)
        save_message(sender, "assistant", reply)

        return respond(reply)

    except Exception as e:
        return respond(f"Hata oluştu:\n{str(e)}")

@app.route("/check", methods=["GET"])
def check_reminders():
    due_reminders = get_due_reminders(grace_minutes=5)
    for r in due_reminders:
        twilio_client.messages.create(
            body=f"🔔 Hatırlatma: {r['message']}",
            from_=TWILIO_FROM,
            to=r["phone"]
        )
    return {"status": "ok", "count": len(due_reminders)}, 200

def respond(message):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>""", 200, {"Content-Type": "application/xml"}
