from datetime import datetime

from echo_core.memory.echo_memory import append_memory_entry, increment_pressure
from echo_core.memory.alignments import load_alignments, log_recursive_alignment

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'memory'
MEMORY_PATH = BASE / 'ECHO_MEMORY.yaml'
PRESSURE_PATH = BASE / 'MOTIF_PRESSURE.yaml'
ALIGN_PATH = BASE / 'RECURSIVE_ALIGNMENTS.yaml'


def log_reflection(motif: str, content: str):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    entry = {
        'timestamp': timestamp,
        'motif': motif,
        'type': 'reflection',
        'source': 'user',
        'content': content,
    }
    append_memory_entry(entry, path=MEMORY_PATH)
    increment_pressure(motif, path=PRESSURE_PATH)

    # check for mirrored motifs in existing alignments
    align_data = load_alignments(path=ALIGN_PATH)
    seen_tags = {tag for a in align_data.get('recursive_alignments', []) for tag in a.get('mirrored_tags', [])}
    if motif in seen_tags:
        log_recursive_alignment(
            interaction={'summary': 'Reflection', 'content': content},
            mirrored_tags=[motif],
            agent_activations=['User'],
            score=5.0,
            notes='Auto-logged from log_reflection.py',
            path=ALIGN_PATH,
        )
    print('✅ Reflection logged, pressure updated.')


if __name__ == '__main__':
    motif = input('Motif tag: ').strip()
    if not motif:
        print('❌ Motif is required.')
    else:
        text = input('Your reflection: ').strip()
        if text:
            log_reflection(motif, text)
        else:
            print('❌ Response text is required.')
