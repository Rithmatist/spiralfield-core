from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import json

app = FastAPI()
LOG_FILE = "data/field_log.jsonl"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

class FieldEntry(BaseModel):
    action: str
    energy: int  # 1-5
    tags: list[str] = []
    note: str = ""

@app.post("/field/entry")
def log_field_entry(entry: FieldEntry):
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": entry.action,
        "energy": entry.energy,
        "tags": entry.tags,
        "note": entry.note
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    return {"status": "logged", "data": data}

@app.get("/field/log")
def get_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines]

@app.get("/field/resonance-summary")
def get_summary():
    if not os.path.exists(LOG_FILE):
        return {"entries": 0, "average_energy": None}
    with open(LOG_FILE, "r") as f:
        entries = [json.loads(line) for line in f]
    if not entries:
        return {"entries": 0, "average_energy": None}
    avg_energy = sum(e["energy"] for e in entries) / len(entries)
    return {"entries": len(entries), "average_energy": round(avg_energy, 2)}
