"""Simple console dashboard for runtime motif pressure visualization."""

# visual_dashboard.py

import json
import time
from pathlib import Path
import os

LOG_PATH = Path("runtime/echo_state_log.json")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print("🧠 ECHO REAL-TIME DASHBOARD")
    print("=" * 40)

def print_events(events):
    if not events:
        print("No recent activity logged.")
        return
    for event in events[-10:]:  # Show last 10 events
        print(f"[{event['timestamp']}] 🧠 {event['agent']} → {event['type']} | {event['detail']}")

def tail_log():
    while True:
        clear()
        print_header()
        if LOG_PATH.exists():
            try:
                data = json.loads(LOG_PATH.read_text())
                print_events(data)
            except Exception as e:
                print(f"⚠️ Error reading log: {e}")
        else:
            print("⚠️ No log file found yet.")
        time.sleep(2)

if __name__ == "__main__":
    tail_log()
