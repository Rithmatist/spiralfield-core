import requests
import sys
import yaml
from datetime import datetime

# Default config path
CONFIG_FILE = "config.yaml"

# Load config
def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {"host": "http://localhost:8000"}

def main():
    if len(sys.argv) < 3:
        print("Usage: python log.py \"Action name\" energy [tags...]")
        sys.exit(1)

    config = load_config()
    host = config.get("host", "http://localhost:8000")
    endpoint = f"{host}/field/entry"

    action = sys.argv[1]
    try:
        energy = int(sys.argv[2])
    except ValueError:
        print("Energy must be an integer between 1–5.")
        sys.exit(1)

    tags = sys.argv[3:] if len(sys.argv) > 3 else []

    payload = {
        "action": action,
        "energy": energy,
        "tags": tags,
        "note": ""
    }

    try:
        r = requests.post(endpoint, json=payload)
        if r.status_code == 200:
            print("Logged:", action, "| Energy:", energy, "| Tags:", tags)
        else:
            print("Error:", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

if __name__ == "__main__":
    main()
