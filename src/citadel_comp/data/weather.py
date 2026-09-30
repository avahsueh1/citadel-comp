"""Download and summarize NOAA's revised Storm Events details snapshots."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

BASE = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
EVENTS = {"Hail": "hail", "Flash Flood": "flash_flood", "Flood": "flood"}
COLUMNS = ["EVENT_ID", "BEGIN_YEARMONTH", "EVENT_TYPE", "STATE_FIPS"]


def fetch(url):
    request = Request(url, headers={"User-Agent": "citadel-comp-public-research/0.1"})
    with urlopen(request, timeout=90) as response:
        return response.read()


def download_years(start, end, destination):
    """Select latest snapshots, cache exact filenames, and record hashes."""
    if start < 1996 or end < start or end >= datetime.now(timezone.utc).year:
        raise ValueError("Use complete calendar years from 1996 through last year.")
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    listing = fetch(BASE).decode()
    records = []
    for year in range(start, end + 1):
        matches = sorted(
            set(re.findall(rf"StormEvents_details-ftp_v1\.0_d{year}_c\d{{8}}\.csv\.gz", listing))
        )
        if not matches:
            raise ValueError(f"No NOAA snapshot found for {year}")
        name = matches[-1]
        path = destination / name
        if not path.exists():
            payload = fetch(BASE + name)
            # Parse before caching so an error page cannot become a data file.
            import gzip
            import io

            pd.read_csv(io.BytesIO(gzip.decompress(payload)), usecols=COLUMNS, nrows=1)
            path.write_bytes(payload)
        records.append(
            {
                "year": year,
                "filename": name,
                "url": BASE + name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "snapshot_date": name.split("_c")[1][:8],
            }
        )
    manifest = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "vintage": "revised_snapshot_not_historical_vintages",
        "files": records,
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def summarize_file(path, year):
    """National event-record counts, not storms, claims, losses, or exposure."""
    rows = pd.read_csv(path, usecols=COLUMNS, low_memory=False)
    if rows.EVENT_ID.duplicated().any():
        raise ValueError("Duplicate NOAA EVENT_ID values")
    months = pd.to_datetime(rows.BEGIN_YEARMONTH.astype(str), format="%Y%m")
    if not months.dt.year.eq(year).all() or set(months.dt.month) != set(range(1, 13)):
        raise ValueError(f"Incomplete or inconsistent year {year}; cannot zero-fill missing months")
    rows["month"] = months
    # State/DC FIPS 1-56 excludes marine zones and territories.
    selected = rows[rows.STATE_FIPS.between(1, 56) & rows.EVENT_TYPE.isin(EVENTS)]
    index = pd.date_range(f"{year}-01-01", f"{year}-12-01", freq="MS")
    result = pd.DataFrame(index=index)
    for event, name in EVENTS.items():
        counts = selected.loc[selected.EVENT_TYPE.eq(event)].groupby("month").size()
        result[name] = counts.reindex(index, fill_value=0).astype(int)
    return result.rename_axis("month").reset_index()


def build_monthly(directory):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text())
    frames = []
    for record in manifest["files"]:
        path = directory / record["filename"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError(f"Source hash mismatch: {path}")
        frames.append(summarize_file(path, record["year"]))
    result = pd.concat(frames).sort_values("month").reset_index(drop=True)
    expected = pd.date_range(result.month.min(), result.month.max(), freq="MS")
    if result.month.tolist() != expected.tolist():
        raise ValueError("Downloaded years must be contiguous and unique")
    return result
