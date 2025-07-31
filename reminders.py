from datetime import datetime, timedelta
import json
import os
import pytz

REMINDERS_FILE = "reminders.json"
ISTANBUL_TZ = pytz.timezone("Europe/Istanbul")

def load_reminders():
    print("[DEBUG] load_reminders çağrıldı")
    if not os.path.exists(REMINDERS_FILE):
        print("[DEBUG] reminders.json bulunamadı")
        return {}
    with open(REMINDERS_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception as e:
            print("[HATA] JSON dosyası yüklenemedi:", e)
            return {}

def save_reminders(reminders):
    print("[DEBUG] save_reminders çağrıldı")
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)
    print("[DEBUG] reminders.json dosyası yazıldı")

def add_reminder(phone_number, time_str, message, original_text):
    print("[DEBUG] add_reminder çağrıldı:", phone_number, time_str)
    reminders = load_reminders()
    print("[DEBUG] load_reminders sonrası:", reminders)
    if phone_number not in reminders:
        reminders[phone_number] = []
    reminders[phone_number].append({
        "time": time_str,
        "message": message,
        "original": original_text
    })
    save_reminders(reminders)
    print("[DEBUG] reminders.json kaydedildi.")

def list_reminders_for_user(phone_number):
    reminders = load_reminders()
    if phone_number not in reminders or len(reminders[phone_number]) == 0:
        return "🔔 Henüz hatırlatıcın yok."
    
    result = "📋 Hatırlatıcıların:\n"
    for r in reminders[phone_number]:
        result += f"- {r['message']}\n"
    return result.strip()

def get_due_reminders(grace_minutes=5):
    now = datetime.now(ISTANBUL_TZ)
    reminders = load_reminders()
    due = []

    for phone, items in reminders.items():
        new_items = []
        for r in items:
            try:
                reminder_time = datetime.fromisoformat(r["time"])
                if reminder_time.tzinfo is None:
                    reminder_time = ISTANBUL_TZ.localize(reminder_time)
                if now >= reminder_time and now - reminder_time <= timedelta(minutes=grace_minutes):
                    due.append({"phone": phone, "message": r["message"]})
                else:
                    new_items.append(r)
            except Exception as e:
                print(f"[HATA] Hatırlatma zamanı işlenemedi: {r['time']} - {str(e)}")
        reminders[phone] = new_items

    save_reminders(reminders)
    return due
