import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "journal", "ECHO_LOG.md")

def _init_log():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            f.write("# 🧠 ECHO Activity Log\n\n")

def log_agent_activation(agent_name: str, action: str = "activated"):
    _init_log()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"- [{timestamp}] **{agent_name}** {action}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)

def log_custom_event(event: str):
    _init_log()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"- [{timestamp}] {event}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)

if __name__ == "__main__":
    # Example usage
    log_agent_activation("CuriosityAgent")
    log_custom_event("🧩 ModulatorAgent weights rebalanced based on 'meta_agency'")
