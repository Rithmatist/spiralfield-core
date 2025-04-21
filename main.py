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

class HookEntry(BaseModel):
    source: str
    event: str
    energy: int
    tags: list[str] = []

@app.post("/field/hook")
def log_hook_entry(entry: HookEntry):
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": f"[{entry.source}] {entry.event}",
        "energy": entry.energy,
        "tags": entry.tags,
        "note": "(auto-logged via hook)"
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    return {"status": "hooked", "data": data}

@app.get("/field/symbolic-log")
def get_symbolic_log():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        entries = [json.loads(line) for line in f]

    try:
        with open("symbol_map.json", "r") as f:
            symbols = json.load(f)
    except FileNotFoundError:
        symbols = {}

    symbolic_entries = []
    for e in entries:
        tag_symbols = [symbols.get(tag, tag) for tag in e.get("tags", [])]
        symbolic_entries.append({
            "timestamp": e["timestamp"],
            "symbols": " ".join(tag_symbols)
        })

    return symbolic_entries

def normalize_tag(tag: str) -> str:
    return tag.strip().lower()

@app.get("/field/tag-resonance")
def get_tag_resonance():
    if not os.path.exists(LOG_FILE):
        return {}

    with open(LOG_FILE, "r") as f:
        entries = [json.loads(line) for line in f]

    tag_data = {}

    for entry in entries:
        energy = entry.get("energy", 0)
        for tag in entry.get("tags", []):
            clean_tag = normalize_tag(tag)
            if clean_tag not in tag_data:
                tag_data[clean_tag] = {"count": 0, "total_energy": 0}
            tag_data[clean_tag]["count"] += 1
            tag_data[clean_tag]["total_energy"] += energy

    for tag in tag_data:
        count = tag_data[tag]["count"]
        total_energy = tag_data[tag]["total_energy"]
        tag_data[tag]["avg_energy"] = round(total_energy / count, 2)
        del tag_data[tag]["total_energy"]

    return tag_data