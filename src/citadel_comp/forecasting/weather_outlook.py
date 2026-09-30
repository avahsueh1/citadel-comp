"""Direct fiscal-quarter weather outlook with a matched stale-data backtest.

These are statistical event-record forecasts, not meteorological forecasts or
predictions of Copart revenue. Model selection ends before the final holdout.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

KEYS = ["hail", "flash_flood", "flood"]


def quarters(monthly):
    data = monthly.copy()
    data["month"] = pd.to_datetime(data.month)
    expected = pd.date_range(data.month.min(), data.month.max(), freq="MS")
    if data.month.tolist() != expected.tolist():
        raise ValueError("Weather months must be sorted, unique and consecutive")
    if not np.isfinite(data[KEYS]).all().all() or (data[KEYS] < 0).any().any():
        raise ValueError("Weather counts must be finite and nonnegative")
    grouped = data.groupby(data.month.dt.to_period("Q-JUL"))
    return grouped[KEYS].sum().loc[grouped.size().eq(3)]


def predict(counts, origin_year, key, method):
    # Same nine-month data gap at every historical and current September origin.
    cutoff = pd.Timestamp(origin_year - 1, 12, 31)
    train = counts.loc[counts.index.end_time.normalize() <= cutoff]
    if len(train) < 16:
        raise ValueError("Need at least four years of complete quarters")
    future = pd.period_range(f"{origin_year + 1}Q2", periods=3, freq="Q-JUL")
    if method == "seasonal_median":
        medians = train.groupby(train.index.quarter)[key].median()
        return np.array([medians.loc[q.quarter] for q in future])
    if method != "ridge_trend":
        raise ValueError("Unknown forecast method")

    def features(index):
        trend = np.array([q.ordinal - train.index[0].ordinal for q in index]) / 40
        return np.column_stack([trend, *[(index.quarter == i) for i in range(1, 5)]])

    model = Ridge(alpha=10)
    model.fit(features(train.index), np.log1p(train[key]))
    return np.maximum(0, np.expm1(model.predict(features(future))))


def outlook(monthly, origin_year=2026):
    counts = quarters(monthly)
    if counts.index[-1].end_time.year >= origin_year:
        raise ValueError("This protocol expects coverage ending in the prior calendar year")
    rows = []
    for year in range(2015, origin_year - 1):
        periods = pd.period_range(f"{year + 1}Q2", periods=3, freq="Q-JUL")
        if not periods.isin(counts.index).all():
            continue
        for key in KEYS:
            forecasts = {
                name: predict(counts, year, key, name)
                for name in ["seasonal_median", "ridge_trend"]
            }
            for i, period in enumerate(periods):
                rows.append({
                    "origin_year": year, "period": str(period), "category": key,
                    "actual": float(counts.loc[period, key]),
                    "partition": (
                        "holdout" if year >= origin_year - 3
                        else "embargo" if year == origin_year - 4 else "development"
                    ),
                    **{name: float(values[i]) for name, values in forecasts.items()},
                })
    results = pd.DataFrame(rows)
    metrics, forward = {}, []
    for key in KEYS:
        sample = results.loc[results.category.eq(key)]
        dev = sample.loc[sample.partition.eq("development")]
        hold = sample.loc[sample.partition.eq("holdout")]
        if len(dev) < 12 or len(hold) < 6:
            raise ValueError("Insufficient development or holdout observations")
        errors = {
            method: float((dev[method] - dev.actual).abs().mean())
            for method in ["seasonal_median", "ridge_trend"]
        }
        chosen = min(errors, key=errors.get)
        # Fixed development residual band: holdout is never used for calibration.
        residuals = (dev[chosen] - dev.actual).abs().to_numpy()
        rank = min(len(residuals), int(np.ceil((len(residuals) + 1) * 0.8)))
        radius = float(np.sort(residuals)[rank - 1])
        coverage = float(((hold[chosen] - hold.actual).abs() <= radius).mean())
        metrics[key] = {
            "selected_method": chosen, "development_mae": errors,
            "holdout_mae": {
                m: float((hold[m] - hold.actual).abs().mean())
                for m in ["seasonal_median", "ridge_trend"]
            },
            "holdout_n": len(hold), "development_n": len(dev),
            "holdout_band_coverage": coverage, "band_radius": radius,
        }
        values = predict(counts, origin_year, key, chosen)
        periods = pd.period_range(f"{origin_year + 1}Q2", periods=3, freq="Q-JUL")
        for period, value in zip(periods, values):
            forward.append({
                "origin": f"{origin_year}-09-30", "period": str(period),
                "category": key, "method": chosen, "forecast": float(value),
                "lower": max(0, float(value) - radius), "upper": float(value) + radius,
            })
    return results, pd.DataFrame(forward), metrics
