# Predictive weather evidence and investment thesis limits

Research forecast dated September 30, 2026. This replaces the historical chart as
the report's main weather figure. The historical chart remains available, with a
blue/orange legend. Forecasting weather alone does not establish investment-thesis
support or competition compliance. The final team-authored investment case still
needs a supported operating forecast and valuation implication.

## What is predicted

U.S. NOAA event-record counts for hail, flash flood and flood in Copart FY2027 Q2
(November 2026–January 2027), Q3 (February–April 2027) and Q4 (May–July 2027).
These are future outcomes at the forecast date. FY2027 Q1 is already in progress
and is deliberately excluded. This is a statistical seasonal outlook, not a
physical weather model or prediction of individual storms.

Source: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/ . Cached source
hashes are in `docs/noaa-source-manifest.json`. Monthly data cover January 2010
through December 2025. Only complete Copart fiscal quarters enter training, so
the final training quarter ends October 2025. No missing 2026 months are replaced
with zero. The stale data reduce the forecast's relevance to current conditions.

## Fixed evaluation protocol

- Candidate 1: expanding historical median for the matching fiscal quarter.
- Candidate 2: ridge regression, alpha 10, on log(1 + quarterly count), with four
  seasonal indicators and a linear trend scaled by 40 quarters. Retransformed
  predictions are nonnegative central estimates, not unbiased expected counts.
- Every forecast origin is September 30. Inputs stop at the prior December,
  matching the same nine-month data gap in the current forecast. Each model is
  refitted only on observations before its cutoff.
- Development origins: 2015–2021, three future quarters each, 21 predictions per
  category. Select the smaller mean absolute error, separately by category.
- Embargo origin: 2022. Its future labels are not all available at the first
  holdout's December 2022 input cutoff, so they cannot select models or bands.
- Holdout origins: 2023 and 2024, six future quarters per category in total. Holdout
  outcomes never select the method or error-band width. Expanding refits can use
  earlier outcomes when they fall before a later origin's input cutoff.
- Error bands use the 18th-smallest absolute development error of 21, the
  finite-sample rank for a nominal 80% range. Lower bounds are clipped to zero.
  Errors are pooled across the three forecast quarters. Seasonality, temporal
  dependence, heteroskedasticity and model selection on development errors mean
  this is an empirical range, not a guaranteed 80% predictive interval.

This protocol was implemented after the underlying dataset existed. These are
retrospective pseudo-out-of-sample results, not a prospectively preregistered test.
NOAA snapshots contain revisions; cutoff rules do not reconstruct historical
publication vintages. There are only two holdout origins, so uncertainty about
performance is substantial.

## Results and thesis implication

All three categories select the seasonal median. On the six holdout quarters,
mean absolute errors are 307.2 hail, 448.6 flash-flood and 186.8 flood records.
Ridge errors are 1297.3, 534.6 and 145.2 respectively. Do not select ridge for flood
after seeing that holdout result: doing so would invalidate the selection test.
Selected error-band coverage is 6/6, 4/6 and 6/6 respectively. Flood/hail coverage
above 80% is not proof of calibration; flash-flood coverage falls below target.

There is no demonstrated ML improvement across this experiment. Seasonal forecasts
are genuinely forward-looking, but they cannot establish a Copart revenue or
valuation advantage. More national weather records do not mechanically imply more
Copart assignments, revenue or profit.

The required next analytical connection is a forecast of quarterly U.S. service
revenue or assignments using publication-dated actuals, compared with a
financial-only benchmark. The existing `weather_cli train` code implements that
comparison, but a sufficient historical Copart target series is still absent.
The supplied workbook's four annual observations cannot replace it. An attempted
SEC companyfacts download on September 30 was blocked by the SEC's automated
access response; no financial observations were invented to fill that gap.

Only after a supported financial relationship is established should the team
change the corresponding quarterly business assumptions and sum to the matching
annual Excel forecast. Apply the workbook's cost and reinvestment assumptions to
obtain cash flow and valuation. Avoid multiplying revenue by weather growth or
counting weather effects already present in the baseline twice. If weather adds
no useful forecast accuracy, retain it as risk analysis and use another supported
operating forecast for the competition's predictive thesis evidence.

## Reproduce

```powershell
.venv/Scripts/python.exe scripts/build_predictive_weather.py
.venv/Scripts/python.exe -m pytest -q
```

Outputs are the PNG/SVG, a row-level backtest, forward forecasts and a JSON report
under `docs/figures/06-*`. Figures have fixed SVG IDs and no variable SVG date.
No sampling is used. Identical inputs and package versions produce identical
figure files. The supplied financial workbook is not modified.

The official competition's AI submission restrictions still apply to this
research draft and its artifacts; Python determinism does not exempt an artifact.
