# Copart investment memorandum

**Research draft for team development, September 30, 2026. AI-assisted text must not be submitted under the competition's rules. The team must independently author the final memorandum.**

**CPRT | Recommendation: [Steven: LONG or SHORT] | Horizon: [3-12 months]**

**Reference price: [verify price and date] | Target price: [after assumption testing] | Expected return: [calculate from final target and reference price]**

## Investment thesis

[Steven: State the recommendation and the specific expectation the market has wrong in two sentences. Identify the business driver, evidence supporting a different outcome, and why that difference should become visible within the investment horizon.]

The central question is whether Copart's recent operating slowdown reflects temporary conditions or a more persistent change in growth and profitability. The accompanying financial model separates service revenue from purchased-vehicle sales and links both businesses to costs, reinvestment, and cash flow. Our recommendation will depend on whether the evidence supports assumptions materially different from the expectations embedded in the share price, and whether those assumptions produce an attractive return profile. The Excel model will be submitted separately; this memorandum summarizes its relevant assumptions and results rather than reproducing its schedules.

## Operating evidence and competitive position

The supplied model records FY2026 revenue of $4,666.2 million, up 0.4% from FY2025, while operating income falls from $1,696.7 million to $1,652.6 million. Operating margin declines from 36.5% to 35.4%. Service revenue is approximately flat at $3,969.5 million, while purchased-vehicle revenue increases 2.7% to $696.7 million. These workbook figures identify the questions the thesis must answer: what drives renewed growth, whether costs can be absorbed more efficiently, and how much reinvestment that improvement requires. FY2026 is labeled unaudited in the source workbook. [1]

[Steven: Add sourced evidence on customer retention, auction competition, buyer participation, management execution, and the economics of repair versus total loss. Select the factors that directly support the thesis. Explain the strongest competing interpretation and why the evidence favors your conclusion.]

## Weather evidence and predictive test

**Methodology.** We aggregate NOAA hail, flash-flood and flood records from 2010-2025 into Copart fiscal quarters. Each FY2025 count is compared with the median for the same quarter number across 63 complete quarters, including FY2025. Percentage deviation equals 100 times (count divided by median minus one). This retrospective comparison uses revised data and does not estimate insured losses or Copart financial outcomes.

Our NOAA analysis measures hail, flash-flood, and flood event records across U.S. states and the District of Columbia. Relative to the median for the same Copart fiscal quarter, all four FY2025 quarters had above-median flash-flood records, while three had below-median hail records. This difference makes a single claim of unusually strong or weak weather insufficient: event type, geography, and the timing of vehicle assignments and auctions may matter. [2]

These observations do not measure insured losses or Copart volumes. The weather regression has not yet been validated against Copart financial actuals, and revised NOAA files do not reconstruct information available at each historical forecast date. The workbook's four annual observations are insufficient for the planned predictive evaluation. Until a longer, preferably quarterly series is tested, weather should remain contextual evidence rather than a numerical earnings uplift.

The September 30, 2026 statistical weather outlook predicts FY2027 Q2–Q4 records.
Seasonal medians beat fixed-penalty ridge regression in development model selection
for all categories. On six separate held-out quarters, selected mean absolute
errors are 307 hail, 449 flash-flood and 187 flood records. Ridge errors are 1,297,
535 and 145 respectively; the better flood holdout result does not justify changing
the previously selected model. Development-based nominal 80% error ranges cover
six, four and six of the respective six holdout outcomes. This small revised-data
test cannot guarantee forward coverage. The forecast uses data through December
2025, with October 2025 the latest complete fiscal quarter. Full protocol and
reproducible forecasts: `docs/predictive-weather-methodology.md` and
`docs/figures/06-weather-forecast-report.json`.

This is a genuine predictive weather component, but the operating and valuation
link is still missing. A weather-count forecast alone cannot establish support
for the team's investment thesis. [Team: supply a supported Copart operating
forecast, compare with a financial-only benchmark and a sourced market expectation,
then quantify its effect on the separate Excel valuation.]

## Valuation and model implications

The separate workbook projects FY2027-FY2031 free cash flow to the firm from after-tax operating profit, depreciation, capital expenditures, and changes in operating working capital. It discounts those cash flows and a terminal value, then adjusts enterprise value for cash, investments, debt, other claims, and shares. The final memo must distinguish a DCF value at the valuation date from a price target over the selected investment horizon. [3]

The current workbook is a starting case, not the team's tested valuation. It holds FY2026 operating ratios and growth assumptions broadly constant, including annual service-revenue growth of approximately 0.02%. At 9.0% WACC and 2.5% terminal growth, its saved standalone output is $23.30 per share, 14.4% below the workbook's $27.22 reference price labeled September 28, 2026. Approximately 73.1% of enterprise value comes from discounted terminal value. These figures require updated thesis assumptions and verification of the provisional cash, debt, and share bridge before becoming a recommendation. [3]

[After testing: replace the starting-case discussion with the supported base case. Report bear/base/bull values and returns, the operating assumptions distinguishing them, and WACC/terminal-growth sensitivity. Explain how the chosen target reconciles with the position and the 3-12 month horizon.]

## Catalysts and risks

[Steven: Identify two dated or clearly bounded catalysts. For each, specify the metric expected to change, the public evidence that will reveal it, and why it could change investor expectations.]

The main thesis risks to test are persistent weakness in service revenue, higher facility or administrative costs, and greater reinvestment requirements than the valuation assumes. The pending ACV transaction is excluded from the workbook's standalone output; its acquisition-adjusted result remains blank. Any transaction case must account for both the consideration paid and the value received, including supported integration costs and synergies. It cannot be represented solely as a cash deduction or an unsupported earnings benefit. [3]

[Team: State the observation that would invalidate the thesis and the resulting downside. For a short recommendation, also address borrow cost, availability, and squeeze risk.]

## References

[1] Separate workbook, *CopartDCFValuationModeL.xlsx*: Historical Data D6:E13 and source notes; Forecast E37:E38. Workbook values inspected September 30, 2026; reconcile to the cited filings and earnings release before submission.

[2] NOAA Storm Events bulk archive, https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/ . Project extract: 2010-2025 revised snapshots; 63 complete fiscal quarters, with same-quarter medians calculated across the full sample, including FY2025. Reproducible exhibit and quarter values: `docs/figures/04-editorial-weather-distribution.svg` and `04-quarter-deviations.csv`.

[3] Separate workbook: Assumptions F6:J35; Forecast F43:J47; Valuation B5:B11, B20:B32, B37:B53; Summary B3:B8 and B22:D25. Numbers above are saved workbook outputs, not a fresh Excel recalculation or independently verified market quote.
