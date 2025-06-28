
# File: agents/critic.py

"""
CriticAgent injects symbolic friction into the cognitive loop by analyzing prompts and motifs
for potential blind spots, overfitting, or false coherence.

It does not create—its role is to challenge. It offers counterpoints, contradictions,
or missing perspectives for a given symbolic motif or generated prompt.

Inputs:
- Top motifs from IntuitionAgent
- Prompt suggestions from NavigatorAgent

Outputs:
- Critical questions or symbolic tensions
- Warnings to avoid recursive resonance traps
"""

class CriticAgent:
    def __init__(self):
        pass

    def critique_motif(self, motif: str) -> str:
        return f"What assumptions underlie the motif '{motif}', and what might it be obscuring?"

    def critique_prompt(self, prompt: str) -> str:
        return f"How might this prompt reinforce an existing bias or overlook an opposing symbolic perspective?"

    def critique(self, motif: str, prompt: str) -> dict:
        return {
            "motif_critique": self.critique_motif(motif),
            "prompt_critique": self.critique_prompt(prompt)
        }

if __name__ == "__main__":
    # Example test
    agent = CriticAgent()
    motif = "resonance_vs_resistance"
    prompt = f"Generate a new prompt exploring the symbolic field: {motif}"
    result = agent.critique(motif, prompt)

    print("🧨 CriticAgent Symbolic Tension Output:")
    print(f"• Motif critique: {result['motif_critique']}")
    print(f"• Prompt critique: {result['prompt_critique']}")
