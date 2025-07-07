# File: agents/motif_dashboard.py
"""Simple console dashboard for displaying motif pressure."""

from pathlib import Path

from echo_core.utils.yaml_utils import load


class MotifDashboard:
    def __init__(self, pressure_file: str | Path | None = None):
        if pressure_file is None:
            pressure_file = Path(__file__).resolve().parents[3] / "memory" / "MOTIF_PRESSURE.yaml"
        self.pressure_file = Path(pressure_file)

    def display(self) -> None:
        data = load(self.pressure_file, fallback={"motif_pressure": {}})
        pressure = data.get("motif_pressure", {})
        print("\n📊 Motif Pressure Dashboard")
        for tag, count in sorted(pressure.items(), key=lambda x: -x[1]):
            print(f"• {tag}: {count}")
