# Citadel competition research

Python workspace for public-data research, operating forecasts, and Monte Carlo valuation. Copart (CPRT) is the initial research candidate; no investment thesis has been validated yet.

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

No data downloader, trained model, simulation, or valuation is implemented yet. The scaffold intentionally contains no invented results.

## Development

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Pytest is available for tests added with implementation. There are no tests yet.

## Competition use

The supplied rules allow disclosed AI assistance for initial research and prohibit generative-AI-generated submission content. This AI-assisted scaffold is a research workspace, not a competition submission. The team should clarify permitted use of AI-assisted code with the organizer before using its outputs in a submission, and independently develop submission materials consistent with the rules.

Keep source citations and provenance. Do not commit credentials, confidential information, downloaded datasets, or large generated artifacts.
