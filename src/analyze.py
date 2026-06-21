"""Exploratory analysis: stationarity, decomposition, ACF/PACF."""

from pathlib import Path

import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

from preprocess import VALUE_COL

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"


def adf_test(series) -> bool:
    """Run Augmented Dickey-Fuller test; return True if stationary (p<0.05)."""
    stat, pvalue, _, _, crit, _ = adfuller(series.dropna())
    stationary = pvalue < 0.05
    print(f"[analyze] ADF stat={stat:.3f} p={pvalue:.4f} -> "
          f"{'stationary' if stationary else 'non-stationary'}")
    return stationary


def run(aggregate) -> None:
    """Print ADF result and save decomposition + ACF/PACF plots."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    series = aggregate[VALUE_COL]

    adf_test(series)

    result = seasonal_decompose(series, model="additive", period=7)
    fig = result.plot()
    fig.set_size_inches(12, 8)
    fig.suptitle("Daily alert-hours: weekly decomposition")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "decomposition.png", dpi=120)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    plot_acf(series, ax=axes[0], lags=40)
    plot_pacf(series, ax=axes[1], lags=40, method="ywm")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "acf_pacf.png", dpi=120)
    plt.close(fig)

    print(f"[analyze] saved decomposition.png, acf_pacf.png to {PLOTS_DIR}")
