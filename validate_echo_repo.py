#!/usr/bin/env python3
try:
    import yaml
except Exception:
    yaml = None
from pathlib import Path

ROOT = Path(__file__).parent

REQUIRED_FILES = [
    ROOT / 'SANCTUARY_SEAL.yaml',
    ROOT / 'belief' / 'TRUTH_EMERGENCE_LOG.yaml',
    ROOT / 'proof' / 'FUTURE_SIGNAL_TREE.yaml',
]

MOTIF_SYMBOLS = ['Δ', '⟲', 'Λ']

def validate_yaml_files():
    missing_headers = []
    missing_symbols = []
    for path in ROOT.rglob('*.yaml'):
        text = path.read_text()
        if yaml is not None:
            try:
                yaml.safe_load(text)
            except Exception as e:
                print(f'YAML syntax error in {path}: {e}')
        first = text.splitlines()[0] if text else ''
        if not first.startswith('#'):
            missing_headers.append(str(path))
        if all(sym not in text for sym in MOTIF_SYMBOLS):
            missing_symbols.append(str(path))
    if missing_headers:
        print('Files missing version headers:')
        for f in missing_headers:
            print(f' - {f}')
    if missing_symbols:
        print('Files lacking motif symbols:')
        for f in missing_symbols:
            print(f' - {f}')

def check_required_files():
    for f in REQUIRED_FILES:
        if not f.exists():
            print(f'Missing required file: {f}')

if __name__ == '__main__':
    validate_yaml_files()
    check_required_files()
