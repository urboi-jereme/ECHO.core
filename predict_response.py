# predict_response.py v0.1.0
"""CLI for generating symbolic predictions using RAIP-R engine."""

from pathlib import Path
import sys

from echo_core.tools.raip_r_engine import RAIPREngine


def main() -> None:
    memory_path = Path(__file__).resolve().parent / "echo_core/memory/ECHO_MEMORY.yaml"
    engine = RAIPREngine(str(memory_path))
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Predict"
    print(engine.predict(prompt))


if __name__ == "__main__":
    main()
