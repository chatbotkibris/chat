import signal
import time
from reminders import get_due_reminders
from twilio.rest import Client
import os

class CancellationToken:
    cancel_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print("Shutdown signal received.")
        self.cancel_now = True

# Twilio setup
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
TWILIO_FROM = os.getenv("TWILIO_PHONE")

def send_reminder(to, message):
    twilio_client.messages.create(
        body=f"🔔 Hatırlatma: {message}",
        from_=TWILIO_FROM,
        to=to
    )

def main():
    token = CancellationToken()

    while not token.cancel_now:
        print("[INFO] Checking reminders...")
        due = get_due_reminders(grace_minutes=5)
        for r in due:
            send_reminder(r["phone"], r["message"])
            print(f"Sent reminder to {r['phone']} - {r['message']}")
        time.sleep(300)

    print("[INFO] Service shut down gracefully.")

if __name__ == "__main__":
    main()

