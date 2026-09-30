# Citadel competition research

Python workspace for public-data research, operating forecasts, and Monte Carlo valuation. Copart (CPRT) is the initial research candidate; no investment thesis has been validated yet.

See [PROJECT_SCOPE.md](PROJECT_SCOPE.md) for the detailed research plan, data requirements, modeling and valuation methods, validation gates, deliverables, and schedule.

## Setup (PowerShell)

Use Python 3.11 or newer.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Optional tree-based ML dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[boosting]"
```

The base project runs on CPU. GPU configuration can be added after confirming the card, VRAM, and workload.

## Layout

```text
configs/                      Human-readable experiment settings
data/raw/                     Original downloaded data (ignored)
data/interim/                 Intermediate transformations (ignored)
data/processed/               Modeling datasets (ignored)
docs/                         Research notes and source register
models/                       Saved fitted models (ignored)
notebooks/                    Exploratory work
outputs/                      Generated results and figures (ignored)
scripts/                      Future pipeline entry points
src/citadel_comp/
    data/                     Data acquisition and cleaning
    features/                 Feature construction and timing controls
    forecasting/              Baselines, ML training, and evaluation
    simulation/               Monte Carlo scenarios and dependence
    valuation/                Business forecasts to equity value
tests/                        Future checks for data and model logic
```

## Research sequence

1. Register public data sources and verify historical availability.
2. Build an interpretable seasonal or regression baseline.
3. Evaluate forecasts on later time periods using only information available at each forecast date.
4. Add ML only if it improves on the baseline out of sample.
5. Translate business-driver scenarios into valuation, making assumptions and correlations explicit.

The initial NOAA weather downloader, monthly feature pipeline, and baseline-versus-weather regression experiment are implemented. See [the weather-model guide](docs/weather-model.md) for commands, historical target requirements, limitations, and the financial-model handoff. No real Copart model has been trained yet; financial actuals are required. Monte Carlo and valuation remain planned.

See [weather research figures](docs/figures/README.md) for sourced PNG/SVG exhibits covering annual history, seasonality, and Copart fiscal-quarter deviations. Regenerate them with `python scripts/build_weather_figures.py` after building the monthly dataset.

## Development

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Run `.\.venv\Scripts\python.exe -m pytest -q` for weather-pipeline and forecast-timing tests. Synthetic fixtures test mechanics only, not investment performance.

## Competition use

The supplied rules allow disclosed AI assistance for initial research and prohibit generative-AI-generated submission content. This AI-assisted scaffold is a research workspace, not a competition submission. The team should clarify permitted use of AI-assisted code with the organizer before using its outputs in a submission, and independently develop submission materials consistent with the rules.

Keep source citations and provenance. Do not commit credentials, confidential information, downloaded datasets, or large generated artifacts.
