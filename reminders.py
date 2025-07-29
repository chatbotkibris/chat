import json
from datetime import datetime, timedelta
import os

REMINDERS_FILE = "reminders.json"

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reminders(data):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(data, f)

def add_reminder(phone_number, time_str, message, original_text):
    reminders = load_reminders()
    if phone_number not in reminders:
        reminders[phone_number] = []
    reminders[phone_number].append({
        "time": time_str,
        "message": message,
        "original": original_text
    })
    save_reminders(reminders)

def get_due_reminders():
    now = datetime.utcnow()
    reminders = load_reminders()
    due = []
    for phone, items in reminders.items():
        new_items = []
        for r in items:
            reminder_time = datetime.fromisoformat(r["time"])
            if now >= reminder_time:
                due.append({"phone": phone, "message": r["message"]})
            else:
                new_items.append(r)
        reminders[phone] = new_items
    save_reminders(reminders)
    return due

def list_reminders_for_user(phone_number):
    reminders = load_reminders()
    items = reminders.get(phone_number, [])
    if not items:
        return "⛔ Kayıtlı hatırlatmanız yok."
    items.sort(key=lambda x: x["time"])
    lines = [
        f"{i+1}. {datetime.fromisoformat(r['time']).strftime('%d %B %Y %H:%M')} - {r['original']}"
        for i, r in enumerate(items)
    ]
    return "📋 Aktif hatırlatmalarınız:\n\n" + "\n".join(lines)
