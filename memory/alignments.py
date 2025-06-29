import os
import yaml
from datetime import datetime

ALIGNMENTS_PATH = os.path.join(os.path.dirname(__file__), 'RECURSIVE_ALIGNMENTS.yaml')

def load_alignments(path: str = ALIGNMENTS_PATH):
    """Load alignment entries from YAML file."""
    if not os.path.exists(path):
        return {'recursive_alignments': []}
    with open(path, 'r') as f:
        data = yaml.safe_load(f) or {}
    if 'recursive_alignments' not in data:
        data['recursive_alignments'] = []
    return data

def save_alignments(data, path: str = ALIGNMENTS_PATH):
    """Persist alignment entries to YAML file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)

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
