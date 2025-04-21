# SpiralField Core

A presence-first field tracking API for resonance, alignment, and clarity over time.

SpiralField Core offers a minimal, open API to log experiences, field tones, and energetic signatures. Designed for Spiral-aligned workflows, but usable by anyone seeking awareness in their daily patterns.

---

## ✨ What it is

- A lightweight backend for presence tracking
- Logs actions, energy states, symbolic tags, or feelings
- Outputs summaries of energetic tone over time
- Optional integrations via webhook or command-line

---

## 🔧 Endpoints

- `POST /field/entry`  
  Submit a moment: action name, energy score (1-5), tags or notes

- `GET /field/log`  
  Retrieve all field entries

- `GET /field/resonance-summary`  
  View average energy and total entries

---

## 🚀 Getting Started

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then visit: `http://localhost:8000/docs`

---

## 🌐 Future Ideas

- Offline-first USB mode
- CLI logging
- Webhook support
- Symbolic encoding + tag resonance charts

---

MIT Licensed. Spiral-anchored. Use freely, modify gracefully.
