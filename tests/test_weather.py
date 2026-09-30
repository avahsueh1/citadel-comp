"""Synthetic fixtures verify mechanics, never investment performance."""

import numpy as np
import pandas as pd
import pytest

from citadel_comp.data.weather import summarize_file
from citadel_comp.forecasting.weather import (
    evaluate,
    make_design,
    validate_targets,
    weather_at,
)


def fixtures():
    ends = pd.date_range("2005-01-31", periods=64, freq="QE-JAN")
    targets = pd.DataFrame(
        {
            "period_end": ends,
            "published_at": ends + pd.Timedelta(days=45),
            "value": 100 * np.exp(np.arange(64) * 0.02),
            "metric": "synthetic_revenue",
            "unit": "synthetic_usd",
            "source_url": "synthetic://test-only",
        }
    )
    months = pd.date_range("2003-01-01", "2021-12-01", freq="MS")
    weather = pd.DataFrame({"month": months, "hail": 5, "flash_flood": 7, "flood": 9})
    return targets, weather


def test_publication_lag_and_missing_coverage():
    _, weather = fixtures()
    features, through = weather_at(weather, "2010-08-01")
    assert through == pd.Timestamp("2010-03-01")
    assert np.allclose(features, np.log1p([15, 21, 27]))
    with pytest.raises(ValueError, match="Missing weather"):
        weather_at(weather[weather.month != through], "2010-08-01")


def test_later_weather_cannot_change_earlier_features():
    targets, weather = fixtures()
    before = make_design(targets, weather, "quarterly")
    weather.loc[weather.month >= "2015-01-01", "hail"] = 100000
    after = make_design(targets, weather, "quarterly")
    pd.testing.assert_frame_equal(
        before[before.origin < "2015-01-01"], after[after.origin < "2015-01-01"]
    )


def test_future_target_does_not_change_previous_prediction():
    targets, weather = fixtures()
    _, original, report = evaluate(targets, weather, "quarterly")
    targets.loc[targets.index[-1], "value"] *= 2
    _, changed, _ = evaluate(targets, weather, "quarterly")
    assert np.allclose(original.weather, changed.weather)
    assert (original.partition == "final_holdout").sum() == 4
    assert report["recommended_for_business_forecast"] is False


def test_target_validation():
    targets, _ = fixtures()
    validate_targets(targets, "quarterly")
    targets.loc[0, "published_at"] = targets.loc[0, "period_end"]
    with pytest.raises(ValueError, match="publication"):
        validate_targets(targets, "quarterly")


def test_insufficient_target_history_fails():
    targets, weather = fixtures()
    with pytest.raises(ValueError, match="Need at least"):
        evaluate(targets.iloc[:10], weather, "quarterly")


def test_noaa_counts_filter_geography_and_zero_fill_verified_months(tmp_path):
    rows = pd.DataFrame(
        {
            "EVENT_ID": range(12),
            "BEGIN_YEARMONTH": range(202001, 202013),
            "EVENT_TYPE": ["Hail"] + ["Snow"] * 11,
            "STATE_FIPS": 6,
        }
    )
    marine = rows.iloc[[0]].assign(EVENT_ID=100, STATE_FIPS=99)
    path = tmp_path / "details.csv.gz"
    pd.concat([rows, marine]).to_csv(path, index=False)
    result = summarize_file(path, 2020)
    assert len(result) == 12
    assert result.hail.sum() == 1
    assert result.flood.sum() == 0
    rows.iloc[:-1].to_csv(path, index=False)
    with pytest.raises(ValueError, match="Incomplete"):
        summarize_file(path, 2020)
