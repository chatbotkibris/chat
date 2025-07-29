import json
import os
from datetime import datetime
import dateparser

REMINDER_FILE = "reminders.json"

def extract_datetime_from_text(text):
    dt = dateparser.parse(text, languages=["tr"])
    return dt

def save_reminder(text):
    dt = extract_datetime_from_text(text)
    if not dt:
        return "Tarih ve saat algılanamadı. Lütfen açık bir şekilde yaz: '1 Ağustos 2025 saat 14:00' gibi."

    reminder = {
        "time": dt.isoformat(),
        "message": f"{dt.strftime('%d %B %Y %H:%M')} için hatırlatma",
        "original": text
    }

    if not os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "w") as f:
            json.dump([], f)

    with open(REMINDER_FILE, "r+") as f:
        data = json.load(f)
        data.append(reminder)
        f.seek(0)
        json.dump(data, f, indent=2)

    return f"🗓️ Randevu kaydedildi: {dt.strftime('%d %B %Y %H:%M')}"
