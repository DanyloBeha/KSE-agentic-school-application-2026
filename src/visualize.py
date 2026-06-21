"""Standalone plots: raw series and per-region heatmap."""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from preprocess import VALUE_COL

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"


def timeseries(aggregate) -> None:
    """Plot the national daily alert-hours series."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(13, 4))
    aggregate[VALUE_COL].plot(ax=ax, color="C3", lw=0.8)
    ax.set_ylabel("alert-hours / day")
    ax.set_title("Ukraine air-raid alert-hours per day (oblast-wide)")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "timeseries.png", dpi=120)
    plt.close(fig)


def heatmap(by_region) -> None:
    """Monthly-resampled region x time heatmap of alert-hours."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    monthly = by_region.resample("ME").sum()
    monthly.index = monthly.index.strftime("%Y-%m")

    fig, ax = plt.subplots(figsize=(14, 9))
    sns.heatmap(monthly.T, cmap="rocket_r", ax=ax,
                cbar_kws={"label": "alert-hours / month"})
    ax.set_xlabel("month")
    ax.set_ylabel("oblast")
    ax.set_title("Air-raid alert-hours by oblast")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "heatmap.png", dpi=120)
    plt.close(fig)

    print(f"[visualize] saved timeseries.png, heatmap.png to {PLOTS_DIR}")
