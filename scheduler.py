import json
import os
import time
from datetime import datetime, timedelta
from twilio.rest import Client
from reminders import get_due_reminders

# Twilio ayarları
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_SID, TWILIO_TOKEN)

def send_reminder(phone, message):
    try:
        client.messages.create(
            body=f"🔔 Hatırlatma: {message}",
            from_=TWILIO_FROM,
            to=phone
        )
        print(f"📨 Gönderildi: {phone} => {message}")
    except Exception as e:
        print(f"❌ Gönderim hatası: {phone} -> {e}")

def run_scheduler():
    print("⏱️ Zamanlayıcı başlatıldı...")
    while True:
        due = get_due_reminders()
        for item in due:
            send_reminder(item["phone"], item["message"])
        time.sleep(60)  # Her dakika çalışır

if __name__ == "__main__":
    run_scheduler()
