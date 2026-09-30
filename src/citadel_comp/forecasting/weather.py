"""Small, auditable weather challenger against a lag-only business baseline."""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

WEATHER = ["hail", "flash_flood", "flood"]
WARNING = (
    "Retrospective revised-weather experiment; assumed 120-day publication lag is not "
    "proof of historical availability. Scenario differences are associations, not causal impacts."
)


def validate_targets(frame, frequency):
    required = {"period_end", "published_at", "value", "metric", "unit", "source_url"}
    if not required.issubset(frame):
        raise ValueError(f"Target file requires {sorted(required)}")
    frame = frame.copy()
    for col in ["period_end", "published_at"]:
        frame[col] = pd.to_datetime(frame[col], errors="raise")
    frame = frame.sort_values("period_end").reset_index(drop=True)
    if frame.empty or frame.period_end.duplicated().any():
        raise ValueError("Target periods must be nonempty and unique")
    for col in ["metric", "unit", "source_url"]:
        if frame[col].isna().any() or frame[col].astype(str).str.strip().eq("").any():
            raise ValueError(f"Missing {col}")
    if frame.metric.nunique() != 1 or frame.unit.nunique() != 1:
        raise ValueError("Use one consistent target metric and unit")
    frame["value"] = pd.to_numeric(frame.value, errors="raise")
    if not np.isfinite(frame.value).all() or (frame.value <= 0).any():
        raise ValueError("Target must be a finite positive level, not a growth rate")
    if (frame.published_at <= frame.period_end).any():
        raise ValueError("Each publication date must follow its period end")
    periods = frame.period_end.dt.to_period("M")
    step = 3 if frequency == "quarterly" else 12
    if any(b.ordinal - a.ordinal != step for a, b in zip(periods, periods[1:])):
        raise ValueError("Target periods must be consecutive fiscal quarters or years")
    if not frame.period_end.dt.is_month_end.all():
        raise ValueError("Use fiscal month-end dates")
    if not frame.period_end.dt.month.isin([1, 4, 7, 10]).all():
        raise ValueError("Quarter ends must match Copart's fiscal calendar")
    if frequency == "annual" and not frame.period_end.dt.month.eq(7).all():
        raise ValueError("Annual Copart targets must end July 31")
    return frame


def weather_at(monthly, origin, lag_days=120):
    if lag_days < 120:
        raise ValueError("This experiment requires at least a 120-day assumed reporting lag")
    data = monthly.copy()
    data["month"] = pd.to_datetime(data.month)
    if data.month.duplicated().any():
        raise ValueError("Duplicate weather months")
    if not np.isfinite(data[WEATHER].to_numpy()).all() or (data[WEATHER] < 0).any().any():
        raise ValueError("Weather counts must be finite and nonnegative")
    origin = pd.Timestamp(origin)
    latest = (origin - pd.Timedelta(days=lag_days)).to_period("M")
    if latest.end_time.normalize() + pd.Timedelta(days=lag_days) > origin:
        latest -= 1
    window = pd.period_range(end=latest, periods=3, freq="M").to_timestamp()
    indexed = data.set_index("month")
    if not window.isin(indexed.index).all():
        raise ValueError(f"Missing weather coverage for {window[0].date()} to {window[-1].date()}")
    return np.log1p(indexed.loc[window, WEATHER].sum()).to_numpy(dtype=float), window[-1]


def make_design(targets, monthly, frequency):
    """Forecast each period on its first day using only earlier published targets."""
    rows = []
    step = 3 if frequency == "quarterly" else 12
    for target in targets.itertuples():
        origin = (target.period_end.to_period("M") - (step - 1)).start_time
        available = targets[targets.published_at < origin]
        if len(available) < 2:
            continue
        try:
            weather, through = weather_at(monthly, origin)
        except ValueError as error:
            if str(error).startswith("Missing weather coverage"):
                continue
            raise
        last, previous = available.iloc[-1], available.iloc[-2]
        seasonal = targets[
            (targets.period_end == target.period_end - pd.DateOffset(years=1))
            & (targets.published_at < origin)
        ]
        if seasonal.empty:
            continue
        phase = (target.period_end.month % 12) / 12 * 2 * np.pi
        rows.append(
            {
                "period_end": target.period_end,
                "published_at": target.published_at,
                "origin": origin,
                "weather_through": through,
                "value": target.value,
                "anchor": float(seasonal.iloc[0].value),
                "lag_growth": np.log(last.value / previous.value),
                "season_sin": np.sin(phase),
                "season_cos": np.cos(phase),
                **dict(zip(WEATHER, weather)),
            }
        )
    return pd.DataFrame(rows)


def fit_model(train, features):
    model = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
    model.fit(train[features], np.log(train.value / train.anchor))
    return model


def evaluate(targets, monthly, frequency):
    design = make_design(targets, monthly, frequency)
    minimum = 24 if frequency == "quarterly" else 10
    base = ["lag_growth"] + (["season_sin", "season_cos"] if frequency == "quarterly" else [])
    predictions = []
    if design.empty:
        raise ValueError("No aligned observations; check source coverage and publication dates")
    for _, row in design.iterrows():
        train = design[(design.published_at < row.origin) & (design.period_end < row.period_end)]
        if len(train) < minimum:
            continue
        test = row.to_frame().T
        result = {
            "period_end": row.period_end,
            "origin": row.origin,
            "actual": row.value,
            "seasonal": row.anchor,
            "training_rows": len(train),
        }
        for name, features in [("baseline", base), ("weather", base + WEATHER)]:
            model = fit_model(train, features)
            result[name] = float(row.anchor * np.exp(model.predict(test[features])[0]))
        predictions.append(result)
    results = pd.DataFrame(predictions)
    if len(results) < 4:
        raise ValueError(
            f"Need at least 4 walk-forward predictions after {minimum} training observations; "
            f"got {len(results)}. Annual 10-K history may be too short; obtain quarterly results."
        )
    results["partition"] = "development"
    results.loc[results.index[-4:], "partition"] = "final_holdout"
    metrics = {}
    for partition, group in [("all", results), *list(results.groupby("partition"))]:
        metrics[partition] = {
            name: {
                "mae": float((group[name] - group.actual).abs().mean()),
                "bias": float((group[name] - group.actual).mean()),
                "n": len(group),
            }
            for name in ["seasonal", "baseline", "weather"]
        }
    # No automatic promotion: small samples and revised inputs need human review.
    return (
        design,
        results,
        {"warning": WARNING, "metrics": metrics, "recommended_for_business_forecast": False},
    )


def scenario_sensitivity(design, frequency):
    """Controlled feature stress, not a calibrated earnings forecast."""
    base = ["lag_growth"] + (["season_sin", "season_cos"] if frequency == "quarterly" else [])
    features = base + WEATHER
    model = fit_model(design, features)
    reference = design.iloc[[-1]][features].copy()
    original = float(model.predict(reference)[0])
    rows = []
    for factor in [0.75, 1.0, 1.25]:
        changed = reference.copy()
        changed[WEATHER] = np.log1p(np.expm1(reference[WEATHER]) * factor)
        delta = float(np.expm1(model.predict(changed)[0] - original))
        rows.append(
            {
                "weather_count_multiplier": factor,
                "relative_target_change": delta,
                "status": "unvalidated_association_stress_not_causal_forecast",
            }
        )
    return pd.DataFrame(rows)
