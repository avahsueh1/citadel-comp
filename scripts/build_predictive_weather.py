"""Generate reproducible forecasts, backtests and a report-ready Python chart."""

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

from citadel_comp.forecasting.weather_outlook import KEYS, outlook


def build():
    root = Path(__file__).resolve().parents[1]
    source = root / "data/processed/weather-monthly.csv"
    destination = root / "docs/figures"
    data = pd.read_csv(source)
    if data.month.tolist() != pd.date_range("2010-01-01", "2025-12-01", freq="MS").strftime(
        "%Y-%m-%d"
    ).tolist():
        raise ValueError("This dated research run requires full 2010–2025 coverage")
    backtest, forward, metrics = outlook(data)
    backtest.to_csv(destination / "06-weather-backtest.csv", index=False)
    forward.to_csv(destination / "06-weather-forecast.csv", index=False)
    report = {
        "origin": "2026-09-30", "data_through": "2025-12-31",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "metrics": metrics,
        "development_origins": "September 2015–2021",
        "embargo_origin": "September 2022",
        "holdout_origins": "September 2023 and 2024",
        "financial_relationship_validated": False,
        "warning": "Revised-data statistical weather outlook; not a Copart revenue forecast. "
        "Development residual ranges have no guaranteed forward probability coverage.",
    }
    (destination / "06-weather-forecast-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "svg.fonttype": "none",
        "svg.hashsalt": "copart-weather-forecast-v1",
    })
    fig, axes = plt.subplots(1, 3, figsize=(11, 5.7))
    fig.subplots_adjust(left=0.09, right=0.98, top=0.70, bottom=0.30, wspace=0.40)
    fig.text(0.06, 0.95, "A forward weather outlook for Copart’s fiscal year", fontsize=19,
             weight="bold", color="#223442", va="top")
    fig.text(0.06, 0.875, "Forecast dated September 30, 2026  •  U.S. event-record counts",
             fontsize=11, color="#52616D")
    fig.legend(handles=[
        Line2D([0], [0], marker="o", color="#227699", linestyle="none", label="Point forecast"),
        Line2D([0], [0], color="#227699", linewidth=3,
               label="Historical error range (nominal 80%; not guaranteed)"),
    ], loc="upper left", bbox_to_anchor=(0.06, 0.84), frameon=False, ncol=2, fontsize=9)
    for ax, key, title in zip(axes, KEYS, ["Hail", "Flash flood", "Flood"]):
        group = forward.loc[forward.category.eq(key)]
        ax.errorbar(range(3), group.forecast,
                    yerr=[group.forecast - group.lower, group.upper - group.forecast],
                    fmt="o", color="#227699", capsize=6, linewidth=2, markersize=6)
        ax.set_xticks(range(3), ["FY27 Q2", "FY27 Q3", "FY27 Q4"], fontsize=9)
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(0, group.upper.max() * 1.2)
        ax.set_title(title, loc="left", fontsize=13, weight="bold")
        ax.tick_params(length=0, labelsize=9)
        ax.grid(axis="y", alpha=0.15)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_ylabel("Event records", fontsize=9)
        for i, value in enumerate(group.forecast):
            ax.annotate(f"{value:,.0f}", (i, value), xytext=(7, 7),
                        textcoords="offset points", fontsize=9, weight="bold")
        method = "Seasonal median" if metrics[key]["selected_method"] == "seasonal_median" \
            else "Ridge trend regression"
        ax.text(0, -0.22, method, transform=ax.transAxes, fontsize=9, color="#52616D")
    fig.text(0.06, 0.15, "Q2: Nov 2026–Jan 2027   |   Q3: Feb–Apr 2027   |   Q4: May–Jul 2027",
             fontsize=10, color="#223442")
    fig.text(0.06, 0.045,
             "Source: NOAA revised 2010–2025 records. Models use complete quarters only; "
             "latest training quarter ends Oct 2025.\n"
             "Model choice and error ranges use development years; final holdout is separate. "
             "Each panel has its own vertical scale.\n"
             "Statistical count outlook, not a storm warning, insured-loss estimate or "
             "Copart revenue forecast.", fontsize=8, color="#52616D", linespacing=1.5)
    for ext in ["png", "svg"]:
        path = destination / f"06-predictive-weather.{ext}"
        fig.savefig(path, dpi=240, facecolor="white",
                    metadata={"Date": None} if ext == "svg" else {})
        if ext == "svg":
            path.write_text("\n".join(line.rstrip() for line in path.read_text(
                encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    build()
