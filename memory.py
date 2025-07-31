from tinydb import TinyDB, Query
from datetime import datetime

# Veritabanını oluştur (kalıcı olarak ana dizinde saklanır)
db = TinyDB("memory_db.json")
Message = Query()

def save_message(user_id, role, content):
    """Kullanıcı mesajını kaydeder (user veya assistant)."""
    db.insert({
        "user_id": user_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
    })

def get_conversation(user_id, limit=10):
    """Son konuşmaları sırayla getirir (user ve assistant mesajları dönüşümlü)."""
    messages = db.search(Message.user_id == user_id)
    messages.sort(key=lambda x: x["timestamp"])
    last_messages = messages[-limit*2:]  # user+assistant çiftleri
    return [{"role": m["role"], "content": m["content"]} for m in last_messages]
