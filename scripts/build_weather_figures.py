"""Export descriptive, report-ready NOAA figures; no financial forecasts."""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

COLORS = ["#235789", "#16817A", "#B56B28"]
NAMES = {"hail": "Hail", "flash_flood": "Flash flood", "flood": "Flood"}
FOOT = (
    "Source: NOAA Storm Events, revised 2010–2025 snapshots; U.S. states/DC. "
    "Extracted September 29, 2026.\n"
    "Counts are event records, not unique storms, insured losses, or Copart volumes. "
    "Reporting practices and revisions may affect comparisons."
)


def finish(fig, title, subtitle, path):
    fig.suptitle(title, x=0.075, y=0.98, ha="left", fontsize=19, fontweight="bold")
    fig.text(0.075, 0.90, subtitle, fontsize=10.5, color="#435366")
    fig.text(0.075, 0.025, FOOT, fontsize=7.5, color="#586474", linespacing=1.6)
    fig.savefig(path.with_suffix(".png"), dpi=220, facecolor="white")
    fig.savefig(path.with_suffix(".svg"), facecolor="white")
    svg = path.with_suffix(".svg")
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def build(source, output):
    data = pd.read_csv(source, parse_dates=["month"])
    expected = pd.date_range("2010-01-01", "2025-12-01", freq="MS")
    if data.month.tolist() != expected.tolist():
        raise ValueError("These report figures require complete ordered 2010–2025 data")
    if not np.isfinite(data[list(NAMES)].to_numpy()).all():
        raise ValueError("Non-finite event counts")
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.labelcolor": "#344254",
            "xtick.color": "#344254",
            "ytick.color": "#344254",
            "svg.fonttype": "none",
        }
    )
    annual = data.groupby(data.month.dt.year)[list(NAMES)].sum()
    fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
    fig.subplots_adjust(left=0.10, right=0.95, top=0.83, bottom=0.15, hspace=0.35)
    for ax, (key, name), color in zip(axes, NAMES.items(), COLORS):
        ax.plot(annual.index, annual[key], color=color, linewidth=2, marker="o", markersize=4)
        ax.set_ylabel(f"{name}\nrecords / year")
        ax.set_ylim(bottom=0)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.grid(axis="y", alpha=0.18)
    axes[-1].set_xticks(range(2010, 2026, 3))
    axes[-1].set_xlabel("Calendar year")
    finish(
        fig,
        "Weather-record counts vary materially from year to year",
        "Annual national event-record counts • separate vertical scales for each series",
        output / "01-annual-weather",
    )

    fig, axes = plt.subplots(1, 3, figsize=(12, 5.5))
    fig.subplots_adjust(left=0.075, right=0.975, top=0.79, bottom=0.23, wspace=0.35)
    for ax, (key, name), color in zip(axes, NAMES.items(), COLORS):
        grouped = data.groupby(data.month.dt.month)[key]
        median = grouped.median()
        ax.fill_between(
            median.index,
            grouped.quantile(0.25),
            grouped.quantile(0.75),
            color=color,
            alpha=0.16,
            label="Middle 50% of years",
        )
        ax.plot(median.index, median, color=color, linewidth=2, label="Median across years")
        ax.set_title(name, loc="left", fontweight="bold")
        ax.set_xticks([1, 4, 7, 10], ["Jan", "Apr", "Jul", "Oct"])
        ax.set_xlabel("Calendar month")
        ax.set_ylabel("Records / month")
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", alpha=0.18)
    axes[0].legend(loc="upper left", fontsize=8, frameon=False)
    finish(
        fig,
        "Seasonality belongs in the baseline before weather is added",
        "Within-month median and interquartile range, 2010–2025 • "
        "descriptive variation, not a confidence interval",
        output / "02-weather-seasonality",
    )

    periods = data.month.dt.to_period("Q-JUL")
    counts = data.groupby(periods)[list(NAMES)].sum()
    complete = data.groupby(periods).size().eq(3)
    counts = counts.loc[complete]
    # Compare each observation with the median for its own fiscal-quarter number.
    relative = counts.copy().astype(float)
    for key in NAMES:
        seasonal_median = counts[key].groupby(counts.index.quarter).transform("median")
        relative[key] = counts[key] / seasonal_median - 1
    recent = relative.loc[relative.index.qyear >= 2022]
    fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
    fig.subplots_adjust(left=0.11, right=0.96, top=0.81, bottom=0.20, hspace=0.32)
    for ax, (key, name), color in zip(axes, NAMES.items(), COLORS):
        ax.bar(range(len(recent)), recent[key] * 100, color=color, width=0.65)
        ax.axhline(0, color="#66717C", linewidth=0.8)
        ax.set_ylabel(f"{name}\nDeviation (%)")
        ax.grid(axis="y", alpha=0.15)
    labels = [f"FY{p.qyear}\nQ{p.quarter}" for p in recent.index]
    axes[-1].set_xticks(range(len(recent)), labels, fontsize=8)
    axes[-1].set_xlabel("Copart fiscal quarter (Q1 ends October; fiscal year ends July)")
    finish(
        fig,
        "Align weather with Copart’s fiscal calendar",
        "Record counts versus the same fiscal quarter’s historical median • "
        "complete quarters only; no financial impact estimated",
        output / "03-fiscal-weather-deviations",
    )
    metadata = {
        "input": str(source),
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "rows": len(data),
        "purpose": "descriptive_research_not_financial_prediction",
        "fiscal_comparison": "same-quarter median across complete quarters within 2010–2025",
        "formats": ["PNG 220 dpi", "SVG vector"],
    }
    (output / "figure-manifest.json").write_text(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("data/processed/weather-monthly.csv"))
    parser.add_argument("--output", type=Path, default=Path("docs/figures"))
    args = parser.parse_args()
    build(args.source, args.output)
