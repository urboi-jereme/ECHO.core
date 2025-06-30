# File: agents/motif_dashboard.py
"""Simple console dashboard for displaying motif pressure."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from yaml_utils import load


class MotifDashboard:
    def __init__(self, pressure_file: str = "memory/MOTIF_PRESSURE.yaml"):
        self.pressure_file = pressure_file

    def display(self) -> None:
        data = load(self.pressure_file, fallback={"motif_pressure": {}})
        pressure = data.get("motif_pressure", {})
        print("\n📊 Motif Pressure Dashboard")
        for tag, count in sorted(pressure.items(), key=lambda x: -x[1]):
            print(f"• {tag}: {count}")
