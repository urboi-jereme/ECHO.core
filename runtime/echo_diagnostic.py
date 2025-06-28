
# File: runtime/echo_diagnostic.py

import os
import yaml

def check_file_exists(path):
    return os.path.exists(path) and os.path.isfile(path)

def check_memory_validity(memory_path):
    if not check_file_exists(memory_path):
        return False, "ECHO_MEMORY.yaml not found."
    with open(memory_path, 'r') as file:
        data = yaml.safe_load(file)
        if not data or 'echo_memory' not in data:
            return False, "ECHO_MEMORY.yaml is malformed or empty."
        if not isinstance(data['echo_memory'], list):
            return False, "ECHO_MEMORY.yaml does not contain a list of memory entries."
    return True, f"Loaded {len(data['echo_memory'])} memory entries successfully."

def check_agents_exist():
    expected_agents = [
        "agents/intuition.py",
        "agents/navigator.py"
    ]
    missing = [agent for agent in expected_agents if not check_file_exists(agent)]
    return missing

def check_journal():
    return check_file_exists("journal/WORKFLOW_JOURNAL.md")

def run_diagnostics():
    print("🧠 Running ECHO.Core Diagnostic Checks...\n")

    memory_ok, memory_msg = check_memory_validity("memory/ECHO_MEMORY.yaml")
    print(f"[{'OK' if memory_ok else 'ERROR'}] Memory Check: {memory_msg}")

    missing_agents = check_agents_exist()
    if missing_agents:
        print(f"[ERROR] Missing agent files: {', '.join(missing_agents)}")
    else:
        print("[OK] All expected agent files found.")

    journal_ok = check_journal()
    print(f"[{'OK' if journal_ok else 'ERROR'}] Journal Check: {'Found WORKFLOW_JOURNAL.md' if journal_ok else 'Missing WORKFLOW_JOURNAL.md'}")

    print("\n✅ Diagnostic completed. Resolve any issues above to maintain recursive system integrity.")

if __name__ == "__main__":
    run_diagnostics()
