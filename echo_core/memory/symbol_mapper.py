from pathlib import Path
from echo_core.utils.yaml_utils import load
MEMORY_PATH = Path(__file__).resolve().parent
MAPPING_FILE = MEMORY_PATH / "SYMBOL_MAPPINGS.yaml"

def load_symbol_mappings():
    if not MAPPING_FILE.exists():
        return {}
    return load(MAPPING_FILE, fallback={})

def resolve_symbol(symbol: str) -> str:
    mappings = load_symbol_mappings()
    return mappings.get(symbol, symbol)  # fallback to self
