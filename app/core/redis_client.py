from typing import List, Dict
import os
import json
import redis

# Use localhost if REDIS_URL is not set
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
r = redis.from_url(REDIS_URL, decode_responses=True)

MEMORY_MAX_TURNS = 40  # keep last N messages

def append_message(session_id: str, role: str, content: str) -> None:
    key = f"chat:{session_id}"
    r.rpush(key, json.dumps({"role": role, "content": content}))
    r.ltrim(key, -MEMORY_MAX_TURNS, -1)

def get_memory(session_id: str) -> List[Dict]:
    key = f"chat:{session_id}"
    items = r.lrange(key, 0, -1)
    return [json.loads(x) for x in items]
