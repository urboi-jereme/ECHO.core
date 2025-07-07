"""Run a small RAIP-R cycle and output beliefs with handshake metadata."""
from pathlib import Path

from echo_core.tools.raip_r_engine import RAIPREngine
from echo_core.tools import belief_export_formatter as bef


def main() -> None:
    memory_path = Path(__file__).resolve().parent / "echo_core/memory/ECHO_MEMORY.yaml"
    engine = RAIPREngine(str(memory_path))
    result = engine.predict("Handshake test")
    yaml_out = bef.format_beliefs(result)
    if not yaml_out:
        print("YAML library missing; raw output:")
        print(result)
    else:
        print(yaml_out)


if __name__ == "__main__":
    main()
