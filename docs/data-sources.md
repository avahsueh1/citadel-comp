# Data source register

## NOAA implementation snapshot (September 29, 2026)

Downloaded complete-year detail files for 2010-2025 from NOAA's official bulk archive and generated 192 monthly U.S. state/DC hail, flood, and flash-flood record-count observations. Exact source URLs, snapshot dates, and hashes are preserved in `noaa-source-manifest.json` beside this document. Raw files and generated datasets remain local and ignored by Git.

These are revised snapshots, not historical publication vintages. A 120-day reporting-lag assumption is used for research features; it does not establish point-in-time correctness. Record counts are not claims, unique storms, or Copart volumes. See `weather-model.md` for commands and limitations. Real Copart target data remains pending.

## Register additional sources

Add an entry for every dataset before using it:

- Publisher and exact source URL
- Retrieval date and applicable access or reuse terms
- Covered dates, geography, units, and field definitions
- Publication lag and revision behavior
- Local file path and transformation steps
- Known gaps and limitations

Candidate sources to assess: company SEC filings and investor disclosures, NOAA storm records, and public industry statistics. Availability and suitability for modeling have not yet been established.

Keep the date an event occurred separate from the date its data became public. Historical backtests must respect the latter. Weather observations are not insurance claims or confirmed Copart volumes.
