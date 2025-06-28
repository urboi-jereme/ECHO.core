import time import os from agents.intuition import IntuitionAgent from agents.navigator import NavigatorAgent from agents.modulator import ModulatorAgent from agents.curiosity_agent import CuriosityAgent from runtime.goal_engine import GoalEngine

from rich.console import Console console = Console()

BASE_PATH = os.path.dirname(os.path.abspath(file)) LOG_FILE = os.path.join(BASE_PATH, "../journal/COGNITION_LOG.md")

def log_to_file(entry): with open(LOG_FILE, "a") as f: f.write(entry + "\n")

def echo_loop(interval=600, silent=False): if not silent: console.print("[bold cyan]\n🔁 ECHO Daemon Active — Autonomous Cognitive Loop[/bold cyan]")

intuition = IntuitionAgent()
modulator = ModulatorAgent()
navigator = NavigatorAgent()
curiosity = CuriosityAgent()
goal_engine = GoalEngine()

while True:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"## 🧠 ECHO Cycle @ {timestamp}\n"

    # Update motif pressure
    motif_data = intuition.get_tag_stats()
    modulator.modulate_weights(motif_data)

    # Ask a question if appropriate
    question = curiosity.ask_question()
    if question:
        if not silent:
            console.print(f"[bold yellow]Curiosity:[/bold yellow] {question}")
        log_entry += f"**Curiosity Question:** {question}\n"

    # Propose goals if motif pressure suggests it
    proposed = goal_engine.propose_goals_from_pressure()
    if proposed:
        if not silent:
            console.print("[bold green]📌 New Goals Proposed:[/bold green]")
        log_entry += "**Proposed Goals:**\n"
        for motif, goal in proposed.items():
            line = f"• {motif}: {goal}"
            log_entry += line + "\n"
            if not silent:
                console.print(line)

    # Plan next steps via Navigator
    plan = navigator.plan_next_steps()
    if not silent:
        console.print("\n[bold blue]🧭 Navigator Suggestions:[/bold blue]")
    log_entry += "**Navigator Suggestions:**\n"
    for p in plan['prompts']:
        log_entry += f"• {p}\n"
        if not silent:
            console.print(f"• {p}")
    for a in plan['actions']:
        log_entry += f"→ {a}\n"
        if not silent:
            console.print(f"[dim]→ {a}[/dim]")

    log_entry += "\n---\n"
    log_to_file(log_entry)

    if not silent:
        console.print(f"\n⏱️ Waiting {interval}s until next cycle...\n")
    time.sleep(interval)

if name == "main": import argparse parser = argparse.ArgumentParser(description="Run ECHO daemon.") parser.add_argument("--silent", action="store_true", help="Run without console output") parser.add_argument("--interval", type=int, default=900, help="Time between cycles in seconds") args = parser.parse_args()

echo_loop(interval=args.interval, silent=args.silent)

