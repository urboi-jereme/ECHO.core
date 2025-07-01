"""Utility for logging user feedback and updating motif pressure."""

from datetime import datetime

from echo_core.memory.echo_memory import append_memory_entry, increment_pressure
from echo_core.memory.alignments import log_alignment


def log_feedback(motif: str, response_text: str) -> None:
    entry = {
        'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'tags': [motif],
        'content': response_text,
        'resonance': 7.0  # Default resonance for feedback
    }
    append_memory_entry(entry)
    increment_pressure(motif)
    # record alignment when user feedback mirrors existing motifs
    log_alignment(
        interaction={
            'summary': f"Feedback for {motif}",
            'content': response_text,
        },
        mirrored_tags=[motif],
        reasoning_path=['feedback', 'motif coherence'],
        agent_activations=['CuriosityAgent'],
        score=7.0,
        notes='Logged from echo_feedback'
    )
    print(f"✅ Feedback on '{motif}' logged successfully. Motif pressure updated.")

if __name__ == "__main__":
    print("✍️  Provide your reflection on a motif.")
    motif = input("Motif tag: ").strip()
    if not motif:
        print("❌ Motif is required.")
        exit(1)
    response = input("Your reflection: ").strip()
    if not response:
        print("❌ Response text is required.")
        exit(1)
    log_feedback(motif, response)
