from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import pytz

# İstanbul saat dilimi
ISTANBUL_TZ = pytz.timezone("Europe/Istanbul")

# Veritabanı dosyası
db = TinyDB("reminders_db.json")
Reminder = Query()


def add_reminder(phone_number, time_str, message, original_text):
    print("[DEBUG] add_reminder çağrıldı:", phone_number, time_str)
    
    # ISO formatlı zamanı datetime objesine çevir
    dt = datetime.fromisoformat(time_str)

    # Zaman dilimi ataması
    if dt.tzinfo is None:
        dt = ISTANBUL_TZ.localize(dt)
    else:
        dt = dt.astimezone(ISTANBUL_TZ)

    # Veritabanına kaydet
    db.insert({
        "phone": phone_number,
        "time": dt.isoformat(),
        "message": message,
        "original": original_text
    })

    print("[DEBUG] reminders_db.json kaydedildi.")
    from pathlib import Path
from tinydb import TinyDB, Query

db_path = Path(__file__).resolve().parent / "reminders_db.json"
db = TinyDB(str(db_path))


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
            reminder_time = reminder_time.astimezone(ISTANBUL_TZ)

            if now >= reminder_time and now - reminder_time <= timedelta(minutes=grace_minutes):
                due.append({"phone": r["phone"], "message": r["message"]})
            else:
                remaining.append(r)

        except Exception as e:
            print(f"[HATA] Hatırlatma zamanı işlenemedi: {r['time']} - {str(e)}")

    # Eski hatırlatmaları temizle, kalanları sakla
    db.truncate()
    db.insert_multiple(remaining)
    
    return due
