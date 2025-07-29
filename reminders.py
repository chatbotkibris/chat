from datetime import datetime, timedelta
import json
import os

REMINDERS_FILE = "reminders.json"

def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return {}
    with open(REMINDERS_FILE, "r") as f:
        return json.load(f)

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)

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

def list_reminders_for_user(phone_number):
    reminders = load_reminders()
    if phone_number not in reminders or len(reminders[phone_number]) == 0:
        return "🔔 Henüz hatırlatıcın yok."
    
    result = "📋 Hatırlatıcıların:\n"
    for r in reminders[phone_number]:
        result += f"- {r['message']}\n"
    return result.strip()

# 👇 BU KISMI EKLİYORSUN:
def get_due_reminders(grace_minutes=5):
    now = datetime.utcnow()
    reminders = load_reminders()
    due = []

    for phone, items in reminders.items():
        new_items = []
        for r in items:
            reminder_time = datetime.fromisoformat(r["time"])
            if now >= reminder_time and now - reminder_time <= timedelta(minutes=grace_minutes):
                due.append({"phone": phone, "message": r["message"]})
            else:
                new_items.append(r)
        reminders[phone] = new_items

    save_reminders(reminders)
    return due
