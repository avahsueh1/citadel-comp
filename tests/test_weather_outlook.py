import numpy as np
import pandas as pd
import pytest

from citadel_comp.forecasting.weather_outlook import KEYS, outlook, predict, quarters


def sample():
    months = pd.date_range("2010-01-01", "2025-12-01", freq="MS")
    return pd.DataFrame({"month": months, **{
        key: 100 + np.arange(len(months)) + 20 * np.sin(months.month * np.pi / 6)
        for key in KEYS
    }})


def test_prediction_cannot_see_future_weather():
    data = sample()
    changed = data.copy()
    changed.loc[changed.month > "2022-12-31", KEYS] *= 100
    for method in ["ridge_trend", "seasonal_median"]:
        np.testing.assert_allclose(
            predict(quarters(data), 2023, "hail", method),
            predict(quarters(changed), 2023, "hail", method),
        )


def test_holdout_cannot_change_selection_or_calibration():
    data = sample()
    changed = data.copy()
    changed.loc[changed.month >= "2023-11-01", KEYS] *= 100
    _, forecast, original = outlook(data)
    _, _, modified = outlook(changed)
    for key in KEYS:
        for field in ["selected_method", "band_radius", "development_mae"]:
            assert original[key][field] == modified[key][field]
        assert original[key]["holdout_n"] == 6
    assert len(forecast) == 9
    assert (forecast.lower >= 0).all()
    assert set(forecast.period) == {"2027Q2", "2027Q3", "2027Q4"}


def test_missing_month_fails_instead_of_becoming_zero():
    with pytest.raises(ValueError, match="consecutive"):
        quarters(sample().drop(index=10))
