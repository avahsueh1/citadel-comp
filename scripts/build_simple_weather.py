"""Deterministic report chart: FY2025 record counts versus seasonal medians."""

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch


def build():
    root = Path(__file__).resolve().parents[1]
    source = root / "data/processed/weather-monthly.csv"
    out = root / "docs/figures"
    data = pd.read_csv(source, parse_dates=["month"])
    if data.month.tolist() != pd.date_range("2010-01-01", "2025-12-01", freq="MS").tolist():
        raise ValueError("Expected complete 2010–2025 monthly data")
    keys = ["hail", "flash_flood", "flood"]
    groups = data.groupby(data.month.dt.to_period("Q-JUL"))
    counts = groups[keys].sum().loc[groups.size().eq(3)]
    median = counts.groupby(counts.index.quarter).transform("median")
    change = 100 * (counts / median - 1)
    recent = change.loc[change.index.qyear == 2025]
    assert len(recent) == 4 and (recent.flash_flood > 0).all()
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "svg.fonttype": "none",
            "svg.hashsalt": "copart-simple-weather-v1",
        }
    )
    fig, axes = plt.subplots(3, 1, figsize=(10, 8.4), sharex=True)
    fig.subplots_adjust(left=0.23, right=0.95, top=0.76, bottom=0.20, hspace=0.57)
    fig.text(
        0.06,
        0.95,
        "FY2025 flash-flood records exceeded\nseasonal norms in every quarter",
        fontsize=21,
        fontweight="bold",
        va="top",
        linespacing=1.2,
        color="#223442",
    )
    fig.text(
        0.06,
        0.835,
        "Change in event-record counts versus the historical median for the same fiscal quarter",
        fontsize=10,
        color="#52616D",
    )
    labels = [
        "Q1   Aug–Oct 2024",
        "Q2   Nov 2024–Jan 2025",
        "Q3   Feb–Apr 2025",
        "Q4   May–Jul 2025",
    ]
    fig.legend(
        handles=[
            Patch(facecolor="#227699", label="Fewer records than seasonal median"),
            Patch(facecolor="#B95F44", label="More records than seasonal median"),
        ],
        loc="upper left",
        bbox_to_anchor=(0.06, 0.815),
        ncol=2,
        frameon=False,
        fontsize=9,
        borderaxespad=0,
        handlelength=1.5,
        columnspacing=2,
    )
    for ax, key, title in zip(axes, keys, ["Hail", "Flash flood", "Flood"]):
        values = recent[key].to_numpy()
        ax.barh(
            range(4), values, height=0.57, color=["#227699" if v < 0 else "#B95F44" for v in values]
        )
        ax.set_yticks(range(4), labels, fontsize=9)
        ax.invert_yaxis()
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold", pad=8)
        ax.axvline(0, color="#68747B", linewidth=1)
        ax.set_xlim(-55, 130)
        ax.set_xticks([-50, 0, 50, 100], ["−50%", "0%", "+50%", "+100%"])
        ax.tick_params(axis="both", length=0, labelbottom=True, labelsize=9, pad=5)
        ax.grid(axis="x", alpha=0.12)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for j, v in enumerate(values):
            ax.text(
                v + (2 if v >= 0 else -2),
                j,
                f"{v:+.0f}%",
                ha="left" if v >= 0 else "right",
                va="center",
                fontsize=10,
                fontweight="bold",
                color="#223442",
            )
    fig.text(
        0.23,
        0.138,
        "0% = historical seasonal median     Left: fewer records     Right: more records",
        fontsize=9,
        color="#52616D",
    )
    fig.text(
        0.06,
        0.093,
        "Example: +106% means about 2.06 times the usual Q3 flash-flood record count"
        "—not a revenue increase.",
        fontsize=9,
        color="#223442",
    )
    fig.text(
        0.06,
        0.035,
        "Source: NOAA Storm Events, revised 2010–2025 data, U.S. states/DC; "
        "retrieved September 29, 2026.\n"
        "Reference: 63 complete fiscal quarters; 15–16 per quarter number, including FY2025.\n"
        "Counts are records, not unique storms, insured losses or Copart volumes. "
        "No financial effect is estimated.",
        fontsize=7.5,
        color="#52616D",
        linespacing=1.5,
    )
    for ext in ["png", "svg"]:
        file = out / f"05-simple-weather-comparison.{ext}"
        fig.savefig(
            file, dpi=240, facecolor="white", metadata={"Date": None} if ext == "svg" else {}
        )
        if ext == "svg":
            file.write_text(
                "\n".join(x.rstrip() for x in file.read_text(encoding="utf-8").splitlines()) + "\n",
                encoding="utf-8",
            )
    plt.close(fig)
    (out / "05-simple-weather-manifest.json").write_text(
        json.dumps(
            {
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "formula": "100 * (count / same-fiscal-quarter full-sample median - 1)",
                "values": {str(p): row.to_dict() for p, row in recent.iterrows()},
                "reference_quarters": len(counts),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    build()
