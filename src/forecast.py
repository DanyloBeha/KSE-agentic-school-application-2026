"""Forecast daily alert-hours with SARIMA and Exponential Smoothing."""

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

import metrics
from preprocess import VALUE_COL

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"

TEST_DAYS = 30
FORECAST_DAYS = 14
SEASON = 7


def _rmse(actual, predicted) -> float:
    return float(np.sqrt(mean_squared_error(actual, predicted)))


def _fit_sarima(series):
    """Fit SARIMA with the shared model config (warnings silenced)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return SARIMAX(
            series,
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, SEASON),
            enforce_stationarity=False,
            enforce_invertibility=False,
        ).fit(disp=False)


def _evaluate(name, actual, predicted) -> dict:
    """Print + return MAE/RMSE for one model; metric key uses the name slug."""
    mae = mean_absolute_error(actual, predicted)
    rmse = _rmse(actual, predicted)
    print(f"[forecast] {name:18s} MAE={mae:7.2f} RMSE={rmse:7.2f}")
    key = name.lower().replace(" ", "_")
    values = {f"{key}_mae": float(mae), f"{key}_rmse": float(rmse)}
    metrics.update(values)
    return values


def run(aggregate) -> None:
    """Fit both models, print test-set metrics, save a forecast plot."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    series = aggregate[VALUE_COL].astype(float)
    train, test = series[:-TEST_DAYS], series[-TEST_DAYS:]

    sarima_pred = _fit_sarima(train).forecast(TEST_DAYS)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ets_pred = ExponentialSmoothing(
            train, trend="add", seasonal="add", seasonal_periods=SEASON
        ).fit().forecast(TEST_DAYS)

    _evaluate("SARIMA", test, sarima_pred)
    _evaluate("ExpSmoothing", test, ets_pred)

    # Refit SARIMA on full series for the forward forecast + CI bands.
    fc = _fit_sarima(series).get_forecast(FORECAST_DAYS)
    mean = fc.predicted_mean
    ci = fc.conf_int()

    fig, ax = plt.subplots(figsize=(13, 5))
    series[-120:].plot(ax=ax, label="observed")
    mean.plot(ax=ax, color="C1", label=f"SARIMA +{FORECAST_DAYS}d")
    ax.fill_between(ci.index, ci.iloc[:, 0], ci.iloc[:, 1],
                    color="C1", alpha=0.2, label="95% CI")
    ax.set_ylabel("alert-hours / day")
    ax.set_title("Air-raid alert-hours forecast (Ukraine, oblast-wide)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "forecast.png", dpi=120)
    plt.close(fig)

    print(f"[forecast] saved forecast.png to {PLOTS_DIR}")


def run_region(by_region, region: str = "Kyiv City") -> None:
    """SARIMA forecast for a single oblast column of by_region.

    Saves plots/forecast_<slug>.png and writes <slug>_mae/_rmse to metrics.
    """
    if region not in by_region.columns:
        print(f"[forecast] region '{region}' not found, skipping")
        return

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    slug = region.lower().replace(" ", "_")
    series = by_region[region].astype(float)
    train, test = series[:-TEST_DAYS], series[-TEST_DAYS:]

    pred = _fit_sarima(train).forecast(TEST_DAYS)
    _evaluate(slug, test, pred)

    fc = _fit_sarima(series).get_forecast(FORECAST_DAYS)
    mean = fc.predicted_mean
    ci = fc.conf_int()

    fig, ax = plt.subplots(figsize=(13, 5))
    series[-120:].plot(ax=ax, label="observed")
    mean.plot(ax=ax, color="C1", label=f"SARIMA +{FORECAST_DAYS}d")
    ax.fill_between(ci.index, ci.iloc[:, 0], ci.iloc[:, 1],
                    color="C1", alpha=0.2, label="95% CI")
    ax.set_ylabel("alert-hours / day")
    ax.set_title(f"{region} air-raid alert-hours forecast")
    ax.legend()
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / f"forecast_{slug}.png", dpi=120)
    plt.close(fig)

    print(f"[forecast] saved forecast_{slug}.png to {PLOTS_DIR}")


def run_long_ets(aggregate, end: str = "2026-12-31") -> None:
    """Long-horizon Exponential Smoothing forecast of the national series.

    Fits damped-trend Holt-Winters on the full series and forecasts to ``end``,
    with a simulated 95% band. Saves plots/forecast_ukraine_ets.png.
    """
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    series = aggregate[VALUE_COL].astype(float)
    horizon = (pd.Timestamp(end) - series.index[-1]).days
    if horizon <= 0:
        print(f"[forecast] series already reaches {end}, skipping long ETS")
        return

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fit = ExponentialSmoothing(
            series, trend="add", damped_trend=True,
            seasonal="add", seasonal_periods=SEASON,
        ).fit()
        mean = fit.forecast(horizon)
        sims = fit.simulate(horizon, repetitions=1000, anchor="end")

    lower = sims.quantile(0.025, axis=1).clip(lower=0)
    upper = sims.quantile(0.975, axis=1)

    # Monthly mean smooths daily noise so a 6-month outlook is readable.
    rule = "ME"
    obs_m = series.resample(rule).mean()
    fc_m = mean.resample(rule).mean()
    lo_m = lower.resample(rule).mean()
    hi_m = upper.resample(rule).mean()
    # Same months one year earlier, aligned onto the forecast x-axis.
    prior_m = obs_m.reindex(fc_m.index - pd.DateOffset(years=1))
    prior_m.index = fc_m.index

    end_value = float(fc_m.iloc[-1])
    metrics.update({"ets_2026_endvalue": end_value,
                    "ets_2026_horizon_days": int(horizon)})
    print(f"[forecast] ETS to {end}: horizon={horizon}d, "
          f"year-end month={end_value:.1f} h/day")

    fig, ax = plt.subplots(figsize=(13, 5))
    obs_m.plot(ax=ax, color="C0", label="observed (monthly mean)")
    fc_m.plot(ax=ax, color="C2", marker="o", ms=3,
              label=f"ETS forecast to {end}")
    ax.fill_between(fc_m.index, lo_m, hi_m, color="C2", alpha=0.18,
                    label="95% band")
    if prior_m.notna().any():
        prior_m.plot(ax=ax, color="C1", ls="--", marker="x", ms=4,
                     label="same months, 2025")

    # Yearly-mean reference lines for trend context.
    for year, val in series.groupby(series.index.year).mean().items():
        ax.axhline(val, color="gray", lw=0.5, ls=":", alpha=0.5)
        ax.text(series.index[0], val, f" {year}", color="gray",
                fontsize=7, va="bottom")

    # Forecast-start divider + year-end annotation.
    ax.axvline(series.index[-1], color="black", lw=0.8, alpha=0.4)
    ax.annotate(f"{end_value:.0f}", xy=(fc_m.index[-1], end_value),
                xytext=(8, 0), textcoords="offset points",
                color="C2", fontweight="bold", va="center")

    ax.set_ylabel("alert-hours / day (monthly mean)")
    ax.set_xlabel("date")
    ax.set_title("All-Ukraine alert-hours — Exponential Smoothing to end 2026")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "forecast_ukraine_ets.png", dpi=120)
    plt.close(fig)

    print(f"[forecast] saved forecast_ukraine_ets.png to {PLOTS_DIR}")
