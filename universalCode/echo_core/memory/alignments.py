from pathlib import Path
from datetime import datetime
from echo_core.utils.yaml_utils import load, dump

ALIGNMENTS_PATH = Path(__file__).resolve().parents[3] / 'memory' / 'RECURSIVE_ALIGNMENTS.yaml'

def load_alignments(path: str | Path = ALIGNMENTS_PATH):
    """Load alignment entries from YAML file."""
    path = Path(path)
    if not path.exists():
        return {'recursive_alignments': []}
    data = load(path, fallback={})
    if 'recursive_alignments' not in data:
        data['recursive_alignments'] = []
    return data

def save_alignments(data, path: str | Path = ALIGNMENTS_PATH):
    """Persist alignment entries to YAML file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dump(data, path)

def _next_alignment_id(entries):
    if not entries:
        return 'A0001'
    last_id = entries[-1].get('id', 'A0000')
    try:
        next_num = int(last_id[1:]) + 1
    except ValueError:
        next_num = len(entries) + 1
    return f"A{next_num:04d}"

def log_alignment(interaction, mirrored_tags, reasoning_path, agent_activations, score, notes, path: str = ALIGNMENTS_PATH):
    """Append an alignment record to RECURSIVE_ALIGNMENTS.yaml."""
    data = load_alignments(path)
    entries = data.get('recursive_alignments', [])
    entry = {
        'id': _next_alignment_id(entries),
        'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'user_interaction': interaction,
        'mirrored_tags': mirrored_tags,
        'reasoning_path': reasoning_path,
        'agent_activations': agent_activations,
        'alignment_score': score,
        'notes': notes,
    }
    entries.append(entry)
    data['recursive_alignments'] = entries
    save_alignments(data, path)
    return entry


def log_recursive_alignment(interaction, mirrored_tags, agent_activations, score, notes, path: str = ALIGNMENTS_PATH):
    """Convenience wrapper that infers the reasoning path from mirrored tags."""
    reasoning_path = [f"mirror:{tag}" for tag in mirrored_tags]
    return log_alignment(
        interaction=interaction,
        mirrored_tags=mirrored_tags,
        reasoning_path=reasoning_path,
        agent_activations=agent_activations,
        score=score,
        notes=notes,
        path=path,
    )
