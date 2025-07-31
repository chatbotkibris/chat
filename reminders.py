from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import pytz
from pathlib import Path

ISTANBUL_TZ = pytz.timezone("Europe/Istanbul")
db_path = Path(__file__).resolve().parent / "reminders_db.json"
db = TinyDB(str(db_path))
Reminder = Query()

def add_reminder(phone_number, time_str, message, original_text):
    print("[DEBUG] add_reminder çağrıldı:", phone_number, time_str)
    db.insert({
        "phone": phone_number,
        "time": time_str,
        "message": message,
        "original": original_text
    })
    print("[DEBUG] reminders_db.json kaydedildi:", db_path)

def list_reminders_for_user(phone_number):
    results = db.search(Reminder.phone == phone_number)
    if not results:
        return "🔔 Henüz hatırlatıcın yok."

    result = "📋 Hatırlatıcıların:\n"
    for r in results:
        result += f"- {r['message']}\n"
    return result.strip()

def get_due_reminders(grace_minutes=5):
    now = datetime.now(ISTANBUL_TZ)
    due = []
    remaining = []

    all_reminders = db.all()

    for r in all_reminders:
        try:
            reminder_time = datetime.fromisoformat(r["time"])
            if reminder_time.tzinfo is None:
                reminder_time = ISTANBUL_TZ.localize(reminder_time)

            if now >= reminder_time and now - reminder_time <= timedelta(minutes=grace_minutes):
                due.append({"phone": r["phone"], "message": r["message"]})
            else:
                remaining.append(r)
        except Exception as e:
            print(f"[HATA] Hatırlatma zamanı işlenemedi: {r['time']} - {str(e)}")

    # önceki verileri temizle ve sadece kalanları yeniden kaydet
    db.truncate()
    db.insert_multiple(remaining)

    return due
