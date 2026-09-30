"""Command-line entry point for weather research."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

from citadel_comp.data.weather import build_monthly, download_years
from citadel_comp.forecasting.weather import evaluate, scenario_sensitivity, validate_targets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    download = commands.add_parser("download")
    download.add_argument("--start-year", type=int, required=True)
    download.add_argument("--end-year", type=int, required=True)
    download.add_argument("--directory", type=Path, default=Path("data/raw/noaa"))
    build = commands.add_parser("build")
    build.add_argument("--directory", type=Path, default=Path("data/raw/noaa"))
    build.add_argument("--output", type=Path, default=Path("data/processed/weather-monthly.csv"))
    train = commands.add_parser("train")
    train.add_argument("--targets", type=Path, required=True)
    train.add_argument("--weather", type=Path, default=Path("data/processed/weather-monthly.csv"))
    train.add_argument("--frequency", choices=["quarterly", "annual"], required=True)
    train.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "download":
        result = download_years(args.start_year, args.end_year, args.directory)
        print(f"Cached {len(result['files'])} NOAA annual snapshots with source hashes.")
    elif args.command == "build":
        data = build_monthly(args.directory)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(args.output, index=False)
        print(f"Wrote {len(data)} monthly rows to {args.output}")
    else:
        targets = validate_targets(pd.read_csv(args.targets), args.frequency)
        weather = pd.read_csv(args.weather)
        design, predictions, report = evaluate(targets, weather, args.frequency)
        args.output.mkdir(parents=True, exist_ok=False)
        design.to_csv(args.output / "design.csv", index=False)
        predictions.to_csv(args.output / "predictions.csv", index=False)
        scenario_sensitivity(design, args.frequency).to_csv(
            args.output / "scenario-sensitivity.csv", index=False
        )
        report["inputs"] = {
            str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [args.targets, args.weather]
        }
        report["frequency"] = args.frequency
        report["metric"] = targets.metric.iloc[0]
        report["unit"] = targets.unit.iloc[0]
        report["python"] = sys.version
        (args.output / "report.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
