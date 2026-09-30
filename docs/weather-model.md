# Weather model: implementation and financial-model handoff

Implemented September 29, 2026. This is an initial research implementation, not evidence that weather predicts Copart's earnings. The friend's financial model and historical input series were not present on `origin/main` when this work began.

## What runs now

1. Download official NOAA Storm Events annual detail snapshots for complete years.
2. Cache originals with source URLs, snapshot dates, and SHA-256 hashes.
3. Verify source hashes and summarize monthly hail, flash-flood, and flood record counts for U.S. states/DC.
4. Accept one historical financial target exported by the team.
5. Align each prediction to the start of its fiscal period, using earlier published financial observations and lagged weather.
6. Compare a seasonal baseline, a regularized lag-only regression, and the same regression with weather features using expanding-window evaluation.
7. Export predictions, errors, and explicitly unvalidated weather scenario sensitivities.

There is no trained real-Copart model until the actual financial target history is supplied. Tests use synthetic financial observations solely to validate code behavior. No synthetic financial results should be cited as research evidence.

## Run in PowerShell

From the repository root, install the project and developer dependencies into a Python 3.11+ virtual environment as described in the main README. The commands below use the local environment directly, so activation is unnecessary.

```powershell
.\.venv\Scripts\python.exe -m citadel_comp.weather_cli download --start-year 2010 --end-year 2025
.\.venv\Scripts\python.exe -m citadel_comp.weather_cli build
.\.venv\Scripts\python.exe -m citadel_comp.weather_cli train --targets data/raw/copart-targets.csv --frequency quarterly --output outputs/weather-first-run
.\.venv\Scripts\python.exe -m pytest -q
```

Use a fresh output directory for every training run. The CLI refuses to overwrite an existing run. Download/build can be rerun; raw filenames are cached and the selected manifest is refreshed. Record the manifest with your research run when comparing data vintages. Downloads currently support complete calendar years only; partial-year coverage is deliberately not treated as a complete zero-filled year.

## Input contract for the financial model

Export historical ACTUALS, not the friend's projected values. Required CSV header:

```text
period_end,published_at,value,metric,unit,source_url
```

- `period_end`: ISO date; Copart fiscal quarter end (January/April/July/October month end), or July 31 for annual observations.
- `published_at`: actual public release date for that observation, not fiscal period end or download date. Must follow period end.
- `value`: positive numeric level, with no commas/currency symbols; choose service revenue, revenue, or units consistently. Do not supply percent growth or cumulative year-to-date values as quarterly levels.
- `metric`: same metric on every row, e.g. `us_service_revenue`. Consolidated revenue is accepted but weakens the geographic link to U.S. weather.
- `unit`: same unit on every row, e.g. `USD_millions`.
- `source_url`: source of the historical observation.

One row per consecutive fiscal period; no duplicate periods, mixed metrics, missing values, or silently interpolated years. If using restated values, publication dates must reflect when those values became available. This initial input format supports one vintage per observation, not a full restatement history; a vintage-aware financial database is future work.

Quarterly is strongly preferred. The model requires 24 aligned training observations before evaluating a quarterly prediction and at least four evaluation predictions. Alignment consumes early history and reporting delays can further reduce the sample, so supply roughly 9-10 years or more if available. Annual mode uses ten aligned training observations plus four evaluation predictions, and often needs 17+ years of raw history. A model built from only three to five annual 10-Ks cannot establish a defensible weather relationship.

Do not repeat an annual target across four quarters to create artificial training samples. Prefer actual 10-Q quarters, or label the analysis annual with its small-sample limitations. If deriving fourth-quarter revenue from annual minus nine-month totals, use the annual release date and document the calculation.

## Exact predictor design

- Forecast origin: first day of the target fiscal quarter/year.
- Reference level: same fiscal period a year earlier, provided it was public before origin.
- Regression response: log(actual target / reference level).
- Baseline features: log growth between the two latest publicly released observations; quarter sine/cosine terms in quarterly mode.
- Weather features: log(1 + total event-record counts) for each of three event categories over the latest three complete months assumed available at origin.
- Assumed reporting delay: month end plus 120 days. Missing required months cause that observation to be excluded, never treated as zero.
- Estimator: training-window standardization followed by ridge regression with fixed alpha 10. No hyperparameter search on the evaluation set.
- Evaluation: expanding windows, restricted by financial publication dates. Final four predictions are labeled final holdout; this is sequential evaluation, so an earlier holdout outcome may train a later forecast once published. Do not tune using holdout performance.
- Report: MAE and signed bias in the target's original units, plus every forecast and its training-row count.

The three-month window and fixed regularization are initial conservative design choices, not optimized or proven economic lags. Annual mode uses the same three-month leading window and is especially limited. Compare alternative designs only on development periods and preserve the original holdout protocol.

## Outputs and integration

- `design.csv`: aligned response, anchors, features, forecast origins, and weather window endpoint.
- `predictions.csv`: actual, seasonal, lag-only, and weather forecasts with evaluation partition.
- `report.json`: errors, caveats, metric/unit, input hashes, and a false-by-default business-use flag.
- `scenario-sensitivity.csv`: weather counts multiplied by 0.75, 1.00, and 1.25 around the last observed design row, with the fitted relative target change.

The scenario multipliers are illustrative stresses, not percentile estimates, hurricane forecasts, or probabilities. The last-row sensitivity uses a model fitted to the full aligned history; it is not a held-out performance result or a forecast for the current period. No current-period forecast is produced by this first version.

Potential handoff, only after validating the relationship and confirming the friend's definitions:

`scenario target = friend's baseline target * (1 + relative target change)`

Do not apply a revenue-trained adjustment to vehicle volumes, margins, or enterprise value. Do not apply a quarterly result directly to annual revenue: adjust each matching quarter and sum levels. Check whether the friend's baseline already includes catastrophe effects; otherwise this can double-count weather. Feed adjusted revenue into their own cost/margin assumptions instead of multiplying every financial line by the same factor.

Automatic integration into the friend's workbook is not implemented because the file, sheet names, forecast periods, units, and intended input cells are unknown. No automatic promotion of weather effects into a business forecast occurs.

## Source limitations

NOAA reference: https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00510

Reporting lag reference: https://www.weather.gov/unr/storm_reports

Bulk data: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/

NOAA reports can arrive 90-120 days late and be revised later. A 120-day delay assumption does not reconstruct the vintage available at a historical date. Accordingly every result here is labeled retrospective revised-weather research. No claim of a truly point-in-time backtest is permitted without vintage evidence.

Counts are event records, not unique storms, insured vehicles, damage severity, Copart assignments, or losses. A large storm may generate many geographic records. National counts are not weighted by insured exposure or Copart market share. Flood categories can relate to the same broader weather system. Reporting practices and geographic coverage can change. This model establishes neither causality nor market mispricing.

The code does not yet isolate customer losses, insurance claim trends, pricing changes, or acquisitions. Those omitted variables can explain apparent weather effects. GPU acceleration would not fix these limitations; this small regression is deliberately CPU-based.

## Next gates

1. Receive the friend's actual historical data and financial model mapping.
2. Reconcile metric definitions and release dates to filings.
3. Run the real target evaluation and inspect whether weather beats both baselines.
4. Check major-storm dependence, reporting changes, and financial structural breaks.
5. If performance is weak, retain the friend's financial forecast and treat weather only as a qualitative risk/scenario.
6. Only after those checks add current-year coverage handling, an explicit forward forecast, exposure weighting, uncertainty intervals, and a workbook adapter.

The competition's AI-assisted research/submission boundary in README.md still applies.
