import yaml
import os
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MEMORY_PATH = os.path.join(BASE_PATH, "memory")

def load_yaml(file_name):
    try:
        with open(os.path.join(MEMORY_PATH, file_name), "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}

def show_motif_pressure():
    pressure = load_yaml("MOTIF_PRESSURE.yaml")
    if not pressure:
        console.print("[bold red]No motif pressure data found.[/bold red]")
        return

    table = Table(title="🔥 Motif Pressure")
    table.add_column("Motif", style="cyan", no_wrap=True)
    table.add_column("Pressure", style="magenta")

    sorted_pressure = sorted(pressure.items(), key=lambda x: x[1], reverse=True)
    for motif, score in sorted_pressure:
        table.add_row(motif, str(score))

    console.print(table)

def show_goals():
    data = load_yaml("GOALS.yaml")
    goals = data.get("goals", [])
    if not goals:
        console.print("[bold red]No goals found.[/bold red]")
        return

    table = Table(title="🎯 Current Goals")
    table.add_column("Motif(s)", style="cyan")
    table.add_column("Goal", style="green")
    table.add_column("Status", style="yellow")

    for entry in goals:
        motifs = ", ".join(entry.get("trigger_tags", ["?"]))
        goal = entry.get("goal", "?")
        status = entry.get("status", "unknown")
        table.add_row(motifs, goal, status)

    console.print(table)

def show_curiosity_log():
    log = load_yaml("CURIOUS_LOG.yaml")
    if not log:
        console.print("[bold red]No curiosity questions found.[/bold red]")
        return

    table = Table(title="❓ Curiosity Log")
    table.add_column("Timestamp", style="dim")
    table.add_column("Motif", style="cyan")
    table.add_column("Question", style="white")
    table.add_column("Answered", style="green")

    for entry in log.get("questions", []):
        ts = entry.get("timestamp", "?")
        motif = entry.get("motif", "?")
        q = entry.get("question_text", "?")
        answered = "✅" if entry.get("user_response") else "❌"
        table.add_row(ts, motif, q, answered)

    console.print(table)

if __name__ == "__main__":
    console.print("[bold underline]🧠 ECHO Visualizer[/bold underline]\n")
    show_motif_pressure()
    show_goals()
    show_curiosity_log()
