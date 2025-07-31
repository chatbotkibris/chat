from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import pytz

db = TinyDB("reminders_db.json")
ISTANBUL_TZ = pytz.timezone("Europe/Istanbul")

def add_reminder(phone_number, time_str, message, original_text):
    db.insert({
        "phone": phone_number,
        "time": time_str,
        "message": message,
        "original": original_text
    })

def list_reminders_for_user(phone_number):
    reminders = db.search(Query().phone == phone_number)
    if not reminders:
        return "🔔 Henüz hatırlatıcın yok."
    
    result = "📋 Hatırlatıcıların:\n"
    for r in reminders:
        result += f"- {r['message']}\n"
    return result.strip()

def get_due_reminders(grace_minutes=5):
    now = datetime.now(ISTANBUL_TZ)
    due = []

    reminders = db.all()
    for r in reminders:
        try:
            reminder_time = datetime.fromisoformat(r["time"])
            if reminder_time.tzinfo is None:
                reminder_time = ISTANBUL_TZ.localize(reminder_time)
            if now >= reminder_time and now - reminder_time <= timedelta(minutes=grace_minutes):
                due.append({"phone": r["phone"], "message": r["message"]})
                db.remove(doc_ids=[r.doc_id])
        except Exception as e:
            print("[HATA] Zaman dönüşümünde hata:", r["time"], str(e))

    return due
