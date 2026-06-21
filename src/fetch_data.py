"""Download and cache the Vadimkin air-raid-sirens dataset."""

from pathlib import Path

import requests

DATA_URL = (
    "https://raw.githubusercontent.com/Vadimkin/"
    "ukrainian-air-raid-sirens-dataset/main/datasets/official_data_en.csv"
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "official_data_en.csv"


def load_or_fetch(force: bool = False) -> Path:
    """Return path to the cached CSV, downloading it first if needed.

    The file is several MB, so it is streamed to disk and cached. Pass
    ``force=True`` to re-download even when a cached copy exists.
    """
    if CSV_PATH.exists() and not force:
        print(f"[fetch] using cached {CSV_PATH.name} "
              f"({CSV_PATH.stat().st_size / 1e6:.1f} MB)")
        return CSV_PATH

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[fetch] downloading {DATA_URL}")
    with requests.get(DATA_URL, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        with open(CSV_PATH, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 16):
                fh.write(chunk)
    print(f"[fetch] saved {CSV_PATH} "
          f"({CSV_PATH.stat().st_size / 1e6:.1f} MB)")
    return CSV_PATH
