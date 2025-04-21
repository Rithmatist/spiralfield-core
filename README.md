# SpiralField Core

A presence-first field tracking API for resonance, alignment, and clarity over time.

SpiralField Core offers a minimal, open API to log experiences, field tones, and energetic signatures. Designed for Spiral-aligned workflows, but usable by anyone seeking awareness in their daily patterns.

---

## ✨ What it is

- A lightweight backend for presence tracking
- Logs actions, energy states, symbolic tags, or feelings
- CLI logging, webhook support, symbolic encoding
- Outputs summaries and resonance maps over time
- Fully local or hostable anywhere

---

## 🔧 Endpoints

- `POST /field/entry`  
  Submit a manual presence log

- `POST /field/hook`  
  Log moments from other apps or automated scripts

- `GET /field/log`  
  View the full log in raw form

- `GET /field/symbolic-log`  
  View logs as compressed tag-symbol sequences (e.g. ✧ ⧉ 〰)

- `GET /field/tag-resonance`  
  Shows frequency + average energy for each tag

- `GET /field/resonance-summary`  
  Overall field energy score

---

## 🌀 CLI Logger (log.py)

Log a presence moment from your terminal:

```bash
python log.py "Aligned meeting" 5 clarity flow
```

You can update the API host via `config.yaml`:

```yaml
host: http://localhost:8000
```

---

## 🕊 Symbol Map

Edit `symbol_map.json` to assign glyphs to tags:

```json
{
  "flow": "〰",
  "clarity": "✧",
  "presence": "⧉"
}
```

---

## 🌱 Installation

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` to explore the live API.

---

## 🛡 .gitignore defaults

The following files are excluded by default:

- `data/field_log.jsonl` (your local log)
- `config.yaml` (personal host settings)
- `__pycache__/`

---

MIT Licensed. Spiral-anchored. Use freely, modify gracefully.