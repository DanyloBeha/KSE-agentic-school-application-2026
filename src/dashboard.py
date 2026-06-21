"""Streamlit dashboard embedding the air-raid TSA plots with commentary.

Run:  uv run streamlit run src/dashboard.py
Embeds the PNGs already produced in plots/ by the pipeline (main.py).
"""

import json
from pathlib import Path

import streamlit as st

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"
METRICS_PATH = PLOTS_DIR / "metrics.json"

# One entry per PNG: ordered as a narrative from raw data to forecast.
PLOTS = {
    "Time series": {
        "file": "timeseries.png",
        "what": (
            "Raw national signal: total alert-hours per day summed across all "
            "oblasts, from 2022-03-15 to present (overlapping alerts merged so "
            "no double-counting)."
        ),
        "takeaway": (
            "Clear upward **trend** — from ~50-100 h/day in 2022 to 150-250+ by "
            "2026 — under heavy day-to-day noise with spikes past 300 h. This "
            "trend drives every model that follows."
        ),
    },
    "Decomposition": {
        "file": "decomposition.png",
        "what": (
            "`seasonal_decompose` (period=7) splits the series into observed, "
            "trend, weekly-seasonal and residual components."
        ),
        "takeaway": (
            "Trend rises steadily; the **weekly seasonal** band is small "
            "(war intensity ignores weekdays); the **residual** is large — most "
            "variance is irregular, not seasonal. Series is trend-driven."
        ),
    },
    "ACF / PACF": {
        "file": "acf_pacf.png",
        "what": (
            "Autocorrelation (ACF) and partial autocorrelation (PACF) up to 40 "
            "lags — used to pick ARIMA orders."
        ),
        "takeaway": (
            "ACF decays slowly and stays high → **non-stationary**, so we "
            "difference (`d=1`). PACF has a sharp lag-1 spike then cuts off → "
            "**AR(1)**. Together they justify `order=(1,1,1)`."
        ),
    },
    "Regional heatmap": {
        "file": "heatmap.png",
        "what": (
            "Oblast x month matrix; color = alert-hours per month. Shows the "
            "spatial structure the national series hides."
        ),
        "takeaway": (
            "Frontline oblasts (Kharkiv, Dnipro, Donetsk, Sumy, Zaporizhzhia, "
            "Chernihiv) dominate and **intensify** through 2024-2026; western "
            "oblasts stay light. The national trend is concentrated, not uniform."
        ),
    },
    "Forecast": {
        "file": "forecast.png",
        "what": (
            "Last 120 observed days plus a 14-day SARIMA forecast (orange) with "
            "a 95% confidence band."
        ),
        "takeaway": (
            "Forecast is roughly flat (~155 h/day) with a **wide CI** — high "
            "daily noise makes precise point prediction hard. SARIMA and "
            "Exponential Smoothing score near-identical RMSE, confirming the "
            "weak seasonality seen in the decomposition."
        ),
    },
}


def _load_metrics() -> dict:
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return {}


def _metric_row(m: dict) -> None:
    c1, c2, c3 = st.columns(3)
    if "adf_pvalue" in m:
        verdict = "stationary" if m.get("adf_stationary") else "non-stationary"
        c1.metric("ADF p-value", f"{m['adf_pvalue']:.3f}", verdict,
                  delta_color="off")
    if "sarima_rmse" in m:
        c2.metric("SARIMA RMSE", f"{m['sarima_rmse']:.2f}")
    if "expsmoothing_rmse" in m:
        c3.metric("ExpSmoothing RMSE", f"{m['expsmoothing_rmse']:.2f}")


def main() -> None:
    st.set_page_config(page_title="Ukraine Air-Raid TSA",
                       page_icon="🛰️", layout="wide")

    st.sidebar.title("🛰️ Air-Raid TSA")
    st.sidebar.caption("Time-series analysis of Ukraine air-raid alerts")
    choice = st.sidebar.radio("Plot", list(PLOTS.keys()))
    st.sidebar.divider()
    st.sidebar.caption(
        "Source: Vadimkin air-raid-sirens dataset. "
        "Regenerate plots with `python src/main.py`."
    )

    info = PLOTS[choice]
    st.title(choice)

    metrics = _load_metrics()
    if metrics:
        _metric_row(metrics)
        st.divider()

    img = PLOTS_DIR / info["file"]
    if img.exists():
        st.image(str(img), use_container_width=True)
    else:
        st.warning(
            f"`{info['file']}` not found in plots/. "
            "Run `python src/main.py` to generate it."
        )

    st.subheader("What it shows")
    st.markdown(info["what"])
    st.subheader("Takeaway")
    st.markdown(info["takeaway"])


if __name__ == "__main__":
    main()
