"""Parse the raw CSV into daily alert-hour time series.

The dataset changed granularity in Dec 2025: before that, alerts were recorded
region-wide (``level == "oblast"``); afterwards they are recorded per
hromada/raion. To get a signal that is consistent across both eras we compute,
for each oblast and day, the *union* of all alert intervals (overlaps merged)
and sum its duration. This is "hours under alert" and never double-counts
concurrent district alerts.
"""

from pathlib import Path

import numpy as np
import pandas as pd

# Column produced by build_series for the value of interest.
VALUE_COL = "alert_hours"

_DAY = np.timedelta64(1, "D")
_HOUR = np.timedelta64(1, "h")


def _load_raw(csv_path: Path) -> pd.DataFrame:
    """Load CSV, parse times as naive UTC, drop rows without a valid interval."""
    df = pd.read_csv(
        csv_path,
        usecols=["oblast", "started_at", "finished_at"],
        parse_dates=["started_at", "finished_at"],
    )
    df = df.dropna(subset=["oblast", "started_at", "finished_at"])
    # Strip timezone (all UTC) so values land on numpy datetime64.
    for col in ("started_at", "finished_at"):
        if df[col].dt.tz is not None:
            df[col] = df[col].dt.tz_convert("UTC").dt.tz_localize(None)
    df = df[df["finished_at"] > df["started_at"]]
    return df


def _union_hours_by_day(starts: np.ndarray, ends: np.ndarray) -> dict:
    """Merge overlapping [start, end) intervals, return {date: hours}.

    ``starts``/``ends`` are numpy datetime64 arrays for a single oblast.
    """
    order = np.argsort(starts)
    starts, ends = starts[order], ends[order]

    out: dict[np.datetime64, float] = {}
    cur_s, cur_e = starts[0], ends[0]
    for s, e in zip(starts[1:], ends[1:]):
        if s <= cur_e:  # overlaps/touches the current merged interval
            if e > cur_e:
                cur_e = e
        else:
            _split_by_day(cur_s, cur_e, out)
            cur_s, cur_e = s, e
    _split_by_day(cur_s, cur_e, out)
    return out


def _split_by_day(s: np.datetime64, e: np.datetime64, out: dict) -> None:
    """Attribute the interval [s, e) to each calendar day it spans."""
    day = s.astype("datetime64[D]")
    while day.astype("datetime64[ns]") < e:
        day_start = day.astype("datetime64[ns]")
        day_end = day_start + _DAY
        seg = min(e, day_end) - max(s, day_start)
        out[day] = out.get(day, 0.0) + seg / _HOUR
        day = day + _DAY


def _to_frame(per_oblast: dict) -> pd.DataFrame:
    """Build a date x oblast hours matrix from {oblast: {date: hours}}."""
    series = {
        oblast: pd.Series(d, dtype=float) for oblast, d in per_oblast.items()
    }
    by_region = pd.DataFrame(series).sort_index()
    by_region.index = pd.to_datetime(by_region.index)
    full_idx = pd.date_range(by_region.index.min(), by_region.index.max(), freq="D")
    return by_region.reindex(full_idx, fill_value=0).fillna(0).rename_axis("date")


def build_series(csv_path: Path):
    """Return (aggregate_df, by_region_df).

    aggregate_df: daily national series, columns [alert_hours, alert_count].
    by_region_df: daily alert_hours pivot, index=date, columns=oblast.
    """
    df = _load_raw(csv_path)

    per_oblast = {
        oblast: _union_hours_by_day(
            g["started_at"].values, g["finished_at"].values
        )
        for oblast, g in df.groupby("oblast", sort=False)
    }
    by_region = _to_frame(per_oblast)
    # The final calendar day is usually incomplete (dataset captured mid-day),
    # which shows up as an artificial dip; drop it.
    by_region = by_region.iloc[:-1]

    # Daily raw alert-event counts (by start date) as a secondary EDA signal.
    counts = (
        df.assign(date=df["started_at"].dt.normalize())
        .groupby("date")
        .size()
        .rename("alert_count")
    )
    aggregate = pd.DataFrame({"alert_hours": by_region.sum(axis=1)})
    aggregate["alert_count"] = counts.reindex(aggregate.index, fill_value=0)

    print(f"[preprocess] {len(df)} alerts -> {len(aggregate)} days, "
          f"{by_region.shape[1]} regions")
    return aggregate, by_region
