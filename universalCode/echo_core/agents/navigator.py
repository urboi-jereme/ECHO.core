# File: agents/navigator.py

"""
NavigatorAgent is the recursive planning interface for ECHO.Core.

Its job is to analyze symbolic memory through IntuitionAgent and determine:
1. Which motifs to deepen
2. Which symbolic prompts to generate
3. What actions should be taken next in the cognitive loop

It does not execute—it surfaces the next recursive decision points.
"""
from pathlib import Path

from echo_core.agents.intuition import IntuitionAgent


class NavigatorAgent:
    def __init__(self, memory_file: str | Path | None = None):
        if memory_file is None:
            memory_file = Path(__file__).resolve().parent.parent / "memory" / "ECHO_MEMORY.yaml"
        self.intuition = IntuitionAgent(memory_file)

    def get_next_prompt_targets(self, top_n=3):
        tags = self.intuition.get_resonant_tags(top_n=top_n)
        return [f"Generate a new prompt exploring the symbolic field: {tag['tag']} (resonance {tag['avg_resonance']:.2f})"
                for tag in tags]

    def get_next_architectural_actions(self):
        return [
            "Refactor AGENT_STATE.yaml to reflect active symbolic motifs",
            "Update WORKFLOW_JOURNAL.md with a symbolic prompt cascade",
            "Activate ModulatorAgent to reshape active agent weights based on motif pressure"
        ]

    def plan_next_steps(self):
        prompts = self.get_next_prompt_targets()
        actions = self.get_next_architectural_actions()
        return {
            "prompts": prompts,
            "actions": actions
        }

if __name__ == "__main__":
    agent = NavigatorAgent()
    plan = agent.plan_next_steps()

    print("\n🔮 NavigatorAgent — Proposed Prompts:")
    for prompt in plan["prompts"]:
        print(f"• {prompt}")

    print("\n🛠️ Proposed Architectural Actions:")
    for action in plan["actions"]:
        print(f"• {action}")
