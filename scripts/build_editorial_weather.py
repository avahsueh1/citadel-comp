"""Editorial distribution exhibit from observed NOAA quarterly record counts."""

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde


def build():
    source = Path("data/processed/weather-monthly.csv")
    output = Path("docs/figures")
    data = pd.read_csv(source, parse_dates=["month"])
    expected = pd.date_range("2010-01-01", "2025-12-01", freq="MS")
    assert data.month.tolist() == expected.tolist(), "Expected complete monthly source"
    keys = ["hail", "flash_flood", "flood"]
    groups = data.groupby(data.month.dt.to_period("Q-JUL"))
    totals = groups[keys].sum().loc[groups.size().eq(3)]
    medians = totals.groupby(totals.index.quarter).transform("median")
    deviations = 100 * (totals / medians - 1)
    recent = deviations.loc[deviations.index.qyear == 2025]
    assert len(recent) == 4
    assert (recent.flash_flood > 0).all()
    assert (recent.hail < 0).sum() == 3
    blue, red, ink, muted = "#26769A", "#C4614F", "#222D35", "#67727B"
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none"})
    fig = plt.figure(figsize=(12, 9.5), facecolor="#FCFBF8")
    fig.text(0.065, 0.974, "COPART  /  WEATHER RESEARCH", fontsize=10, color=muted, weight="bold")
    fig.text(
        0.065,
        0.875,
        "Flash-flood activity stood out in FY2025.\nHail told a different story.",
        fontsize=27,
        fontfamily="DejaVu Serif",
        color=ink,
        linespacing=1.2,
    )
    fig.text(
        0.065,
        0.803,
        "All four FY2025 quarters had above-median flash-flood records; "
        "three had below-median hail.\n"
        "Each quarter is compared with the historical median for the same Copart fiscal quarter.",
        fontsize=11,
        color=muted,
        linespacing=1.6,
    )
    ygrid = np.linspace(-100, 370, 700)
    panels = [
        ("hail", "Hail", "3 of 4", "quarters below median", blue),
        ("flash_flood", "Flash flood", "4 of 4", "quarters above median", red),
        ("flood", "Flood", "3 of 4", "quarters below median", blue),
    ]
    for i, (key, name, count, note, accent) in enumerate(panels):
        left = 0.065 + i * 0.31
        fig.text(left, 0.743, name, fontsize=16, weight="bold", color=ink)
        fig.text(left, 0.697, count, fontsize=23, color=accent, weight="bold")
        fig.text(left + 0.105, 0.704, note, fontsize=9, color=muted)
        ax = fig.add_axes([left, 0.23, 0.27, 0.435], facecolor="#FCFBF8")
        values = deviations[key].to_numpy()
        density = gaussian_kde(values)(ygrid)
        density = density / density.max() * 0.25
        # A half-density is an explicitly smoothed distribution, not a count axis.
        ax.fill_betweenx(ygrid, -density, 0, where=ygrid >= 0, color=red, alpha=0.18)
        ax.fill_betweenx(ygrid, -density, 0, where=ygrid <= 0, color=blue, alpha=0.18)
        rng = np.random.default_rng(42)
        jitter = rng.uniform(0.035, 0.16, len(values))
        ax.scatter(jitter, values, s=14, color="#A4ADB2", alpha=0.65, linewidths=0)
        points = sorted([(float(row[key]), f"Q{p.quarter}") for p, row in recent.iterrows()])
        # Move labels only; leader lines retain exact observed marker positions.
        label_y = []
        for value, _ in points:
            label_y.append(max(value, label_y[-1] + 22) if label_y else value)
        for (value, quarter), label in zip(points, label_y):
            color = red if value > 0 else blue
            ax.scatter(
                [0.21], [value], s=42, color=color, edgecolors="white", linewidths=0.9, zorder=5
            )
            ax.plot([0.235, 0.36], [value, label], color=color, alpha=0.65, linewidth=0.8)
            ax.text(
                0.38,
                label,
                f"{quarter}  {value:+.0f}%",
                va="center",
                fontsize=9,
                color=color,
                bbox={"facecolor": "#FCFBF8", "edgecolor": "none", "pad": 1},
                zorder=6,
            )
        ax.axhline(0, color="#7F878B", linewidth=0.8, linestyle=(0, (2, 3)))
        ax.set_ylim(-100, 370)
        ax.set_xlim(-0.31, 0.85)
        ax.set_xticks([])
        ax.set_yticks([-100, 0, 100, 200, 300], ["−100%", "0", "+100%", "+200%", "+300%"])
        ax.tick_params(axis="y", length=0, labelsize=8, colors=muted, pad=3)
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.text(
        0.065,
        0.19,
        "Vertical scale: deviation in event-record counts from the same-quarter historical median.",
        fontsize=10,
        color=ink,
    )
    fig.text(
        0.065,
        0.163,
        "Gray dots: complete historical quarters  •  Labeled dots: FY2025  •  "
        "Shading: smoothed distribution",
        fontsize=9,
        color=muted,
    )
    fig.text(
        0.065,
        0.131,
        "Above/below median describes weather records—not a "
        "favorable/unfavorable financial outcome.",
        fontsize=9,
        color=muted,
        style="italic",
    )
    fig.text(
        0.065,
        0.062,
        "Source: NOAA Storm Events, U.S. states/DC; revised 2010–2025 snapshots "
        "retrieved September 29, 2026.\n"
        "Reference: 63 complete fiscal quarters (15–16 per quarter number), including FY2025. "
        "FY2025: Aug 2024–Jul 2025.\n"
        "Records are not unique storms, insured losses, or Copart volumes. "
        "This descriptive exhibit does not estimate earnings impact.",
        fontsize=8,
        color=muted,
        linespacing=1.65,
    )
    output.mkdir(parents=True, exist_ok=True)
    for ext in ["png", "svg"]:
        path = output / f"04-editorial-weather-distribution.{ext}"
        fig.savefig(path, dpi=240, facecolor=fig.get_facecolor())
        if ext == "svg":
            path.write_text(
                "\n".join(s.rstrip() for s in path.read_text(encoding="utf-8").splitlines()) + "\n",
                encoding="utf-8",
            )
    plt.close(fig)
    deviations.rename_axis("fiscal_quarter").to_csv(output / "04-quarter-deviations.csv")
    (output / "04-editorial-manifest.json").write_text(
        json.dumps(
            {
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "reference_quarters": len(totals),
                "highlight_fiscal_year": 2025,
                "density": "Gaussian KDE, Scott bandwidth; each panel normalized to own peak",
                "jitter": "Horizontal jitter is decorative only, deterministic seed 42",
                "interpretation": "Full-sample description, not a point-in-time backtest",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    build()
