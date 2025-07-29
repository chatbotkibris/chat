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

    # Her kullanıcı için ayrı liste
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
