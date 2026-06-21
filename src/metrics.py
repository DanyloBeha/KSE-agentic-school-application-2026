"""Shared metrics sink: merge key numbers into plots/metrics.json."""

import json
from pathlib import Path

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"
METRICS_PATH = PLOTS_DIR / "metrics.json"


def update(values: dict) -> None:
    """Merge ``values`` into plots/metrics.json (create if missing)."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    data = {}
    if METRICS_PATH.exists():
        data = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    data.update(values)
    METRICS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load() -> dict:
    """Return saved metrics, or empty dict if none."""
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return {}
