"""Forecast daily alert-hours with SARIMA and Exponential Smoothing."""

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

from preprocess import VALUE_COL

PLOTS_DIR = Path(__file__).resolve().parent.parent / "plots"

TEST_DAYS = 30
FORECAST_DAYS = 14
SEASON = 7


def _rmse(actual, predicted) -> float:
    return float(np.sqrt(mean_squared_error(actual, predicted)))


def _evaluate(name, actual, predicted) -> None:
    mae = mean_absolute_error(actual, predicted)
    rmse = _rmse(actual, predicted)
    print(f"[forecast] {name:18s} MAE={mae:7.2f} RMSE={rmse:7.2f}")


def run(aggregate) -> None:
    """Fit both models, print test-set metrics, save a forecast plot."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    series = aggregate[VALUE_COL].astype(float)
    train, test = series[:-TEST_DAYS], series[-TEST_DAYS:]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        sarima = SARIMAX(
            train,
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, SEASON),
            enforce_stationarity=False,
            enforce_invertibility=False,
        ).fit(disp=False)
        sarima_pred = sarima.forecast(TEST_DAYS)

        ets = ExponentialSmoothing(
            train, trend="add", seasonal="add", seasonal_periods=SEASON
        ).fit()
        ets_pred = ets.forecast(TEST_DAYS)

    _evaluate("SARIMA", test, sarima_pred)
    _evaluate("ExpSmoothing", test, ets_pred)

    # Refit SARIMA on full series for the forward forecast + CI bands.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        full = SARIMAX(
            series,
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, SEASON),
            enforce_stationarity=False,
            enforce_invertibility=False,
        ).fit(disp=False)
    fc = full.get_forecast(FORECAST_DAYS)
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
