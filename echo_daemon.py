import time from agents.intuition import IntuitionAgent from agents.navigator import NavigatorAgent from agents.modulator import ModulatorAgent from agents.curiosity_agent import CuriosityAgent from runtime.goal_engine import GoalEngine

from rich.console import Console console = Console()

def echo_loop(interval=600): console.print("[bold cyan]\n🔁 ECHO Daemon Active — Autonomous Cognitive Loop[/bold cyan]")

intuition = IntuitionAgent()
modulator = ModulatorAgent()
navigator = NavigatorAgent()
curiosity = CuriosityAgent()
goal_engine = GoalEngine()

while True:
    console.rule("🧠 ECHO CYCLE")

    # Update motif pressure
    motif_data = intuition.get_tag_stats()
    modulator.modulate_weights(motif_data)

    # Ask a question if appropriate
    question = curiosity.ask_question()
    if question:
        console.print(f"[bold yellow]Curiosity:[/bold yellow] {question}")

    # Propose goals if motif pressure suggests it
    proposed = goal_engine.propose_goals_from_pressure()
    if proposed:
        console.print("[bold green]📌 New Goals Proposed:[/bold green]")
        for motif, goal in proposed.items():
            console.print(f"• {motif}: {goal}")

    # Plan next steps via Navigator
    plan = navigator.plan_next_steps()
    console.print("\n[bold blue]🧭 Navigator Suggestions:[/bold blue]")
    for p in plan['prompts']:
        console.print(f"• {p}")
    for a in plan['actions']:
        console.print(f"[dim]→ {a}[/dim]")

    # Sleep until next cycle
    console.print(f"\n⏱️ Waiting {interval}s until next cycle...\n")
    time.sleep(interval)

if name == "main": echo_loop(interval=900)  # Run every 15 minutes

