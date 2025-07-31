# memory.py
from tinydb import TinyDB, Query

memory_db = TinyDB("conversation_memory.json")

def save_message(phone, role, content):
    memory_db.insert({"phone": phone, "role": role, "content": content})

def get_conversation(phone, limit=10):
    messages = memory_db.search(Query().phone == phone)[-limit:]
    return [{"role": m["role"], "content": m["content"]} for m in messages]
