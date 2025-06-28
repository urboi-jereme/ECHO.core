import yaml
import os

MEMORY_PATH = os.path.join(os.path.dirname(__file__))
MAPPING_FILE = os.path.join(MEMORY_PATH, "SYMBOL_MAPPINGS.yaml")

def load_symbol_mappings():
    if not os.path.exists(MAPPING_FILE):
        return {}
    with open(MAPPING_FILE, "r") as f:
        return yaml.safe_load(f) or {}

def resolve_symbol(symbol: str) -> str:
    mappings = load_symbol_mappings()
    return mappings.get(symbol, symbol)  # fallback to self
