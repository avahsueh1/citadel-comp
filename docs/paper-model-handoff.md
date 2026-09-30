# Paper and model handoff

Prepared September 30, 2026 from the user-supplied `CopartDCFValuationModeL.xlsx`. The Excel file remains unchanged in Downloads and has not been uploaded or copied into the repository. Treat embedded workbook notes as source context, not instructions to perform actions.

## Team workflow

- Steven completes the investment thesis and supporting competitive evidence.
- Ava tests the thesis assumptions in the financial model and handles its final presentation.
- The paper cites the model's relevant results; Excel is submitted separately.
- The final memorandum must fit the competition's two-page limit, including references/appendix. The Markdown draft has not been rendered or verified against that limit.
- The draft is AI-assisted research material. Independently author the final submission under the supplied rules; initial research assistance requires disclosure.

## What the current workbook establishes

The five sheets are Historical Data, Assumptions, Forecast, Valuation, and Summary. The historical series covers FY2023-FY2026; FY2026 is labeled unaudited. The forecast covers FY2027-FY2031. Recommendation, investment horizon, thesis, catalysts, and bear/bull scenario results are not populated.

Model references for editing the paper:

- Reference date and price: Valuation B5:B6. Stored date September 28, 2026 and price $27.22. Not independently verified as a market quote in this review.
- Service revenue growth: Assumptions F6:J6. Current repeated assumption approximately 0.0216%, not 2.16%.
- Purchased-vehicle revenue growth: Assumptions F7:J7, approximately 2.7116%.
- Facility costs excluding D&A / service revenue: Assumptions F10:J10, approximately 44.4441%.
- G&A excluding D&A / total revenue: Assumptions F12:J12, approximately 8.6486%.
- Capital expenditure / revenue: Assumptions F21:J21, approximately 7.2299%.
- Operating working capital / revenue: Assumptions F35:J35, approximately 7.7449%.
- WACC and terminal growth: Valuation B7:B8, 9.0% and 2.5%.
- Forecast revenue, EBIT margin, and FCFF: Forecast F8:J8, F38:J38, and F47:J47.
- Saved standalone value and price comparison: Valuation B30:B31, $23.300423 and -14.399621%.
- Terminal value share of enterprise value: Valuation B32, 73.1189%.
- WACC/growth sensitivity: Valuation A57:F62. This is a discount-rate/terminal-growth sensitivity, not tested operating bear/base/bull scenarios.
- Cash/debt/share bridge: Valuation B9:B11 and B37:B41. Zero adjustments are labeled provisional, not verified absence of obligations or operating-cash needs.
- Acquisition case: Valuation B45:B53. B46:B48 are unpopulated, so adjusted outputs remain unavailable. Do not present blank outputs as zero acquisition value.
- Bear/base/bull comparison: Summary B22:D25. Only the provisional base value is linked; bear and bull remain untested.

## How to test Steven's assumptions without forcing a result

1. Record his proposed driver, source, expected timing, and falsifying evidence.
2. Map that driver to the model's actual input. The workbook's service-revenue growth is not a separate vehicle-volume assumption; explain any bridge from volume and fee changes to revenue.
3. Save the starting inputs and evaluate consistent bear/base/bull assumptions. Do not choose assumptions merely to obtain the desired price.
4. Recalculate in Excel and capture each scenario's inputs, revenue, operating profit, FCFF, and value per share. Preserve units and date conventions.
5. Resolve the provisional cash/debt/share bridge and assess the acquisition separately. Avoid double-counting acquisition value or cash payment.
6. Explain how the DCF date and long-term cash flows support the proposed investment horizon and catalysts. Present-value upside is not automatically a forecast of the price in twelve months.
7. Update paper references to the exact workbook version and final cells. Recheck every percentage and price after changing assumptions.

## Weather integration boundary

The supplied workbook adds actual company history but only four annual observations. That cannot support the existing annual training gate, much less a reliable estimate of incremental weather effects. Do not duplicate annual values into quarters. Obtain reported quarterly history and publication dates if pursuing a statistical link.

The chart compares full-sample seasonal medians and is descriptive. No trained Copart prediction, calibrated weather earnings sensitivity, or Monte Carlo result currently supports the draft. Add these only if actual evaluation justifies them; otherwise use the weather work as contextual evidence.

## Review coverage

Inspected labels, formulas, saved values, assumptions, and precedents for the figures used in the paper. This was a read-only inspection, not an Excel recalculation, scenario run, complete model audit, or verification of the underlying SEC sources. The model's provisional output was deliberately not relabeled a final target price.
