# Project scope: Copart operating forecasts and Monte Carlo valuation

Status: proposed research plan, not a validated investment recommendation.

Created: September 21, 2026. Target first-round deadline: October 2, 2026, 11:59:59 p.m. Eastern Time, according to the supplied competition rules. All internal deadlines below use Pacific Time unless stated otherwise.

This document specifies work to be done. Named modules, commands, datasets, and outputs below are planned unless explicitly described as existing. It does not claim that models, data pipelines, backtests, or investment results already exist.

## 1. Objective and decision to produce

Investigate whether Copart's recent operating weakness is temporary, structural, or a combination, and determine whether the current share price implies a materially different outlook from the evidence.

The desired research outcome is a defensible long, short, or no-conviction conclusion for CPRT over a 3-12 month investment horizon. Use a 12-month valuation endpoint for the primary analysis, with identifiable evidence updates over the next 3-6 months. The competition ultimately requires a long or short recommendation; a no-conviction research outcome means reconsidering the security rather than inventing a position.

The project must connect five things:

1. A specific disagreement with expectations embedded in the share price.
2. Public evidence that measures the relevant business drivers.
3. A forecast that can be evaluated against a simple baseline.
4. An understandable bridge from operating outcomes to equity value.
5. Catalysts that could resolve the disagreement within the investment horizon.

Success is not a high model score alone, a large simulation count, or GPU utilization. Success is a traceable explanation of what the market would need to be wrong about and how much that disagreement matters to valuation.

## 2. Competition boundaries and authorship

Source: the user-supplied `Citadel-Fall-2026-Pitch-Competition-Official-Rules.pdf`, especially pages 1-3. The PDF is not copied into this repository.

- Eligible securities: ABNB, ADBE, CPRT, GEV, NCLH, NKE, SBUX, and SPOT.
- Teams: 2-4 eligible undergraduate students. Each team member's eligibility must be checked against the full rules.
- Interest-form deadline: September 18, 2026. Team registration status is unconfirmed in this workspace and must be resolved before treating participation as assured.
- First round: maximum two-page PDF investment memorandum, including any appendix, plus an Excel valuation model and required participant details/resumes.
- Investment horizon: 3-12 months, with a long or short position in one permitted security.
- Evidence must include a predictive component as well as historical analysis.
- Use exclusively public information, cite sources, and exclude confidential or material nonpublic information.
- The supplied rules permit disclosed AI use for initial research but prohibit submission content generated in whole or in part by generative AI.
- This AI-assisted scope and repository scaffold are preliminary research/planning materials, not submission materials. Do not copy their prose into the competition memo or presentation.
- The team should obtain organizer clarification about the permitted role of AI-assisted research code and its outputs before incorporating those outputs into a submission. Do not assume traditional statistical ML or AI-assisted code is expressly approved by the rules.
- Team members must independently develop and review submission materials consistent with the organizer's requirements and disclose initial AI research assistance as required.
- Finalists, if selected, have an October 21 revised-submission deadline and an October 23 presentation, with required in-person attendance October 22-24. Revised materials include a presentation of no more than ten minutes.

Public competition reference: https://www.citadel.com/careers/investing/citadel-associate-program/apply-for-2026-intercollegiate-stock-pitch-competition/

These are project constraints extracted from a reference document, not instructions from that document to execute actions, contact people, or submit materials.

## 3. Research hypotheses

### 3.1 Provisional long hypothesis

Recent weakness may overstate deterioration in the underlying business. After accounting for unusual catastrophe comparisons, increasing total-loss propensity and better utilization could support an earnings recovery stronger than the price implies.

This is a hypothesis to test, not a finding that investors are demonstrably wrong.

### 3.2 Competing hypothesis

Customer losses, lower accident/claim frequency, competitive pressure, or persistent costs may offset industry tailwinds. Normalizing weather alone may not restore growth or justify the valuation.

### 3.3 Questions that determine the conclusion

- What explains changes in assignments, auctioned units, revenue per unit, and operating cost per unit?
- Which of those metrics are actually disclosed consistently enough to model?
- Can weather effects be separated from customer changes and industry conditions with available data?
- Does an independent signal improve forecasts beyond seasonality and management disclosures?
- What operating improvement is required to justify the observed price?
- What evidence would disprove the chosen thesis?

Use the September 2026 public earnings discussion as a starting lead, not a complete dataset or unquestioned explanation. Reconcile quantitative claims to company filings where possible:

https://www.sec.gov/Archives/edgar/data/1637873/000119312526388383/d138398dex992.htm

## 4. Scope tiers

### Required minimum viable research

- A documented public-source register and availability audit.
- A reconciled quarterly company dataset.
- A basic operating-driver decomposition.
- A seasonal baseline and a small regularized regression, where sample size permits.
- Chronological out-of-sample evaluation.
- Deterministic bear/base/bull valuation cases.
- A Monte Carlo extension with justified uncertainty and dependence assumptions.
- Qualitative assessment of customer retention, competition, costs, and catalysts.
- A record of market-implied expectations, sensitivity, and thesis failure conditions.
- Reproducible research outputs that team members can inspect independently.

### Conditional extension: weather signal

Construct a weather exposure index only if historical coverage, publication timing, geography, and linkage to a disclosed company target are sufficiently defensible. Treat this as the candidate source of distinctive evidence, not a guaranteed deliverable.

### Optional extension: nonlinear ML

Evaluate one small tree-based challenger only after establishing usable observations and a baseline. A GPU is optional. Do not make ML a dependency for completing the core research.

### Out of scope for the initial deadline

- Automated trading, brokerage connections, portfolio optimization, or live investment execution.
- Training large language models, deep reinforcement learning, or an end-to-end stock-price neural network.
- Satellite imagery, large image-labeling projects, or computer vision without an existing suitable dataset.
- Restricted scraping, private insurance records, purchased alternative data without separately approved access, or confidential interviews.
- Claims that millions of weather rows provide millions of independent company earnings observations.
- A production website or dashboard; exported charts and research files are sufficient.
- AI-generated final competition memo, slide deck, or submission-ready workbook.

## 5. Data acquisition and availability audit

### 5.1 Company fundamentals: required

Candidate sources: Copart investor relations, annual/quarterly SEC filings, earnings releases, and public earnings transcripts.

https://www.copart.com/Content/US/EN/Investor-Relations

Target at least 32 comparable fiscal quarters, preferably 40 or more, ending at the latest publicly reported period available before the selected information cutoff. Do not manufacture historical metrics to meet this target. Document reporting changes, acquisitions, restatements, stock splits, and missing disclosures.

Collect where available:

- U.S., international, and consolidated revenue and operating income.
- Service revenue separately from purchased-vehicle revenue.
- Service or auction volumes, assignment volumes, and inventory measures.
- Reported volume growth, when absolute units are unavailable.
- Fee/revenue per unit only where numerator and denominator are comparable.
- Facility and operating costs with clearly recorded definitions.
- Cash, investments, debt, other relevant claims, and diluted shares.
- Capital expenditure, depreciation, taxes, and working-capital measures needed for valuation.
- Disclosed catastrophe adjustments, customer changes, and material transactions.

Never equate auction gross merchandise value, auction selling price, and Copart's recognized fee revenue. Never mix assignment timing with sold-unit timing without an explicit lag model.

### 5.2 Industry indicators: required to assess; include only usable series

Candidates: publicly released collision/claim frequency, total-loss frequency, repair severity, vehicle miles traveled, used-vehicle prices, and relevant cost indices.

For each candidate, verify historical depth, public accessibility, release dates, measurement definition, and allowed reuse. Public commentary about a proprietary series does not establish that its full history is freely available.

Do not multiply vehicle miles traveled by a claim-frequency series already measured per insured vehicle without aligning denominators. A conceptual volume bridge is insured exposure times claims per exposure times total-loss share times Copart capture share, adjusted for timing and other business sources. Some components may remain scenario assumptions rather than estimable series.

### 5.3 Weather: conditional

Candidate source: NOAA Storm Events Database and documented bulk files:

- https://www.ncei.noaa.gov/access/storm-events-database
- https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/

Start with hail and flood events. Track event time, available location, event type, intensity proxies, publication/revision timing, and missingness. Storm counts and property-damage estimates are not observed auto claims.

Possible exposure weights, in priority order:

1. Public vehicle-exposure measures at a compatible geographic level.
2. Transparent population-based proxies, with limitations disclosed.
3. Unweighted regional indices as a baseline.

Facility proximity can be a robustness exercise, but a nearby Copart facility does not prove that affected vehicles route there. Current facility locations must not be silently used as historical locations. If opening dates are unavailable, label historical geographic analysis as approximate and do not claim a tradable historical test.

### 5.4 Price, expectations, and valuation inputs

Obtain a public, timestamped CPRT share price and record currency, exchange session, adjustment conventions, and source. Use historical prices with split-consistent share counts if comparing historical valuations.

Use publicly accessible consensus only if its source, coverage, timestamp, and definition can be documented. Otherwise solve for expectations implied by the price under an explicit valuation framework. Do not label that calculation as analyst consensus.

### 5.5 Source and observation schemas

Maintain `docs/data-sources.md` and a machine-readable source manifest. Each source entry should record:

- `source_id`, publisher, exact URL, retrieval timestamp, access/reuse notes.
- Covered period, geography, unit definitions, release schedule, known revisions.
- Raw local filename, file hash, parser version, and limitations.

Each observation should retain:

- `entity`, `metric`, `period_start`, `period_end`, `value`, `unit`.
- `published_at`, `retrieved_at`, `source_id`, and source locator.
- `segment`, `geography`, and adjustment notes where relevant.

Missing values remain missing with a documented reason. Explicitly distinguish zero, not reported, not applicable, and not yet published.

## 6. Research design and feature engineering

### Primary target selection

Prefer U.S. service-volume growth if a consistent series is available. Otherwise use U.S. service-revenue growth and acknowledge that volume and price effects cannot be fully separated. Lock the target after the feasibility audit, before testing candidate models.

Forecast the next reported fiscal quarter as the primary statistical task. Extend valuation over the next four quarters with explicit assumptions and uncertainty; do not claim validated 12-month forecast accuracy from a one-quarter backtest.

### Candidate features

- Target lags and fiscal-quarter seasonality.
- Lagged industry claim frequency and total-loss measures.
- Used-vehicle pricing and cost proxies with known availability dates.
- Lagged weather exposure over preselected monthly windows.
- Separately documented event indicators for material customer or business changes.

Limit the initial regression to a small number of economically motivated features, approximately 3-5 beyond basic seasonality depending on usable observations. Do not search hundreds of lag combinations on a few dozen quarters.

Aggregate calendar observations into Copart fiscal periods explicitly. Join every feature using its public availability date relative to the forecast origin. Fit scalers, imputers, and transformations only on the training window.

### Weather identification limits

Use weather primarily as a predictive covariate. A positive association is not proof of a causal earnings effect. Compare alternative geographic weights, leave major storm periods out in robustness checks, and report whether performance is dominated by one event.

Revised weather records retrieved today may contain information unavailable historically. If original vintages cannot be reconstructed, identify the result as a retrospective association study rather than a fully point-in-time backtest. Such evidence cannot support claims of historically achievable forecasting performance.

## 7. Forecasting and validation

### Models, in order

1. Seasonal naive: use the comparable quarter from the prior year for a level target, or a documented seasonal rule for a growth target.
2. Small regularized linear regression: economically interpretable features, conservative regularization.
3. Optional shallow gradient-boosted trees with strict complexity limits.

Do not fit a neural network to quarterly company data. A regional panel is an option only if independently observed regional target labels exist; repeating the national target across counties creates pseudo-observations and is prohibited.

### Evaluation protocol

- Aim for at least 24 training quarters before the first evaluation origin and eight sequential evaluation quarters if data permit.
- Use expanding-window evaluation; never randomly split time-series rows.
- Keep the latest four observable quarters as a final holdout, not used for feature/model selection.
- Use only earlier rolling windows for any hyperparameter tuning.
- If data cannot support this design, simplify the model and explicitly downgrade confidence; do not invent synthetic historical observations.
- Report MAE, median absolute error, signed bias, per-origin predictions, and baseline-relative error. Express growth-target errors in percentage points.
- Avoid MAPE where the target is zero or near zero.
- Report interval coverage and width where predictive intervals are used; acknowledge limited sample precision.

### ML acceptance gate

Before final holdout evaluation, set a provisional practical hurdle: at least a 10% reduction in rolling validation MAE versus the stronger simple baseline, with improvement not explained by a single unusual quarter. This threshold is a project decision rule, not a claim of statistical significance.

Report final holdout results even if unfavorable. Keep the simple model if the challenger fails to generalize. Preserve unsuccessful experiments to prevent selective reporting.

## 8. Operating model and valuation

### Operating bridge

For each forecast quarter, build an auditable sequence:

1. Relevant auction/service volumes or disclosed growth rates.
2. Recognized revenue per service unit, where identifiable.
3. Service revenue and purchased-vehicle revenue modeled separately.
4. Variable costs, fixed costs, and resulting operating profit.
5. Taxes and other items appropriate to the valuation method.

If a component is undisclosed, use a labeled assumption or a reduced-form revenue model. Do not present inferred unit economics as company-reported figures.

Model U.S. and international operations separately to the extent data support them; a U.S. weather signal does not forecast all consolidated operations. Reconcile segment totals to consolidated results.

### Primary valuation

Use a forward enterprise-value-to-EBIT framework, subject to confirming that the financial definitions support it:

`endpoint equity value = endpoint operating enterprise value + excess cash/investments - debt - other applicable claims`

`endpoint price = endpoint equity value / endpoint diluted shares`

The multiple must match the earnings period: at a 12-month endpoint, a forward multiple applies to earnings forward from that endpoint. If those additional forecasts are too speculative, use a clearly labeled trailing measure at the endpoint and matching comparable multiples.

Record cash deployment, repurchases, share changes, and material transaction scenarios explicitly. Avoid counting cash as both spent on an acquisition and still available to shareholders. Do not import unreconciled transaction assumptions from an old snapshot.

Use a compact DCF as a cross-check only if cash-flow assumptions are sufficiently supported and time permits. Avoid presenting an unexplained average of conflicting valuation methods.

### Market-implied expectations

At the selected price, solve for the growth, margin, or multiple needed to justify that price while holding other assumptions explicit. Compare these requirements with evidence-supported ranges. Multiple combinations can explain one price; show this ambiguity rather than claiming one uniquely implied forecast.

### Position logic

A potential long requires sufficient upside under defensible assumptions and tolerable downside. A potential short requires a supported downside case plus treatment of borrow cost, dividends owed, squeeze risk, and timing; do not assume short borrow is available or free. No trading implementation is included.

## 9. Monte Carlo specification

### Purpose

Propagate uncertainty in operating drivers and valuation assumptions into a distribution of endpoint equity values. Do not simulate stock-price paths from arbitrary historical volatility and call that a fundamental thesis test.

### Uncertain quantities

- Forecast residuals or volume/revenue growth uncertainty.
- Fee or revenue-per-unit changes, if estimable.
- Cost behavior and margins.
- Weather-related contribution, only where supported.
- Customer retention or transaction outcomes as explicit discrete scenarios where warranted.
- Endpoint valuation multiple.

Use empirical residual resampling when supported. Use bounded scenario distributions for assumptions without reliable estimates, clearly labeled as judgment. Do not count the same forecast uncertainty once in driver shocks and again in a full residual shock.

Preserve dependence using jointly resampled residual vectors, a simple validated covariance model, or explicitly linked scenarios. Include sensitivity to dependence assumptions. In weak operating scenarios, examine whether valuation multiples also compress rather than assuming independence by default.

### Runs and reproducibility

- Begin with 10,000 simulations and a fixed recorded random seed.
- Increase to 50,000 or 100,000 only if estimates are unstable.
- Check multiple seeds. Proposed numerical convergence criterion: median return changes by less than 0.5 percentage points and the 10th/90th percentile returns by less than 1 percentage point across larger batches.
- Report failure to converge; more paths reduce sampling noise, not model misspecification.
- Separate uncertainty about parameters from variation in business outcomes where practical.

### Required outputs

- Median, 10th, and 90th percentile endpoint value and return.
- Conditional modeled probability of a loss and of a predeclared material loss threshold, initially 20%.
- Bear/base/bull cases alongside the probabilistic result.
- Sensitivity ranking of the assumptions that drive value.
- Explicit statement that probabilities are conditional on model choices and are not calibrated guarantees of investment performance.

## 10. Qualitative workstream

Create `docs/thesis-evidence.md` with one entry per material claim:

- Claim and investment relevance.
- Supporting public evidence and precise citation.
- Contrary evidence and alternative explanation.
- Metric that could validate or invalidate it.
- Potential timing of that evidence.
- Confidence and unresolved questions.

Investigate:

1. Customer retention: pricing, service, logistics, switching incentives, and disclosed account changes.
2. Competitive position: auction buyer participation, seller outcomes, and alternatives to Copart.
3. Facilities and costs: whether capacity and service spending create benefits or persistently dilute returns.
4. Management credibility: compare prior measurable statements with subsequent reported outcomes.
5. Industry economics: repair costs, vehicle values, insurance behavior, and competing effects on total losses.
6. Capital allocation: cash deployment, buybacks, acquisitions, and the assumptions needed to earn adequate returns.

No unverified claim that the market has ignored a factor. Distinguish an interesting fact from an earnings driver and an earnings driver from mispricing.

Maintain `docs/catalysts-and-risks.md`. For each catalyst record the event, expected window, public date source if available, metric to watch, and why it might change expectations. Verify earnings dates before naming a specific date; otherwise use a tentative window.

## 11. Technical implementation plan

Existing: package directories, dependency metadata, setup instructions, and artifact exclusions. The following files are proposed:

```text
configs/cprt.toml
docs/thesis-evidence.md
docs/catalysts-and-risks.md
docs/experiment-log.md
src/citadel_comp/data/manifest.py
src/citadel_comp/data/company.py
src/citadel_comp/data/weather.py
src/citadel_comp/features/quarterly.py
src/citadel_comp/features/availability.py
src/citadel_comp/forecasting/baselines.py
src/citadel_comp/forecasting/regression.py
src/citadel_comp/forecasting/evaluate.py
src/citadel_comp/simulation/scenarios.py
src/citadel_comp/valuation/operating.py
src/citadel_comp/valuation/equity.py
scripts/build_dataset.py
scripts/run_forecasts.py
scripts/run_valuation.py
```

Implement scripts only after input schemas are agreed. Each should accept an explicit configuration path and write to a unique run directory. Acquisition should be separate from analysis so a frozen dataset can reproduce results without fresh network requests.

Each configuration should record the ticker, information cutoff, target, horizon, fiscal calendar, split boundaries, feature set, model settings, seed, valuation inputs, scenario assumptions, and output path. Validate types and required fields; stop on missing inputs rather than substituting invented defaults.

Each run should record configuration, source hashes, Git commit, package versions, data vintage, execution timestamp, forecast outputs, metrics, and assumptions. Create a tested dependency lock or exact environment snapshot once implementation starts; the current version ranges are not a reproducibility lock.

Use pandas/NumPy and simple scikit-learn models first. Add XGBoost only for the optional challenger. Confirm exact GPU model, VRAM, driver, and compatible library versions before enabling acceleration. A report of a "5080 TI" is not a verified hardware specification.

Keep the entire minimum pipeline runnable on CPU. Benchmark any GPU path against CPU using the same inputs and report differences within a documented numerical tolerance. No runtime or speedup claims before measurement.

## 12. Tests and quality controls

Add meaningful tests when implementing the corresponding behavior:

- Company line items reconcile across segments and reporting periods.
- Fiscal-quarter aggregation handles date boundaries correctly.
- Availability joins exclude observations published after the forecast origin.
- Missing source data cannot silently become zero.
- Train/test boundaries and fitted transformations prevent future-data leakage.
- Stock-split treatment, units, and share counts are consistent.
- Fixed-cost and variable-cost bridges reconcile with operating profit.
- Enterprise-to-equity calculations handle debt, cash, and shares correctly.
- Simulations reproduce with a fixed seed and produce finite, economically interpretable outputs.
- Correlation/covariance inputs are valid; truncation and impossible values are handled transparently.
- Scenario tests have expected directional effects when other assumptions are fixed.

Use tiny synthetic fixtures for accounting and boundary tests, explicitly labeled synthetic. Do not use them as investment evidence or forecast validation. Run lint, relevant tests, and an end-to-end frozen-data run before accepting an implemented milestone.

## 13. Deliverables and acceptance criteria

### A. Data audit

Deliver a source register, schema, coverage summary, missingness report, and target-selection decision. Accept only when source timing and key metric definitions are documented and the chosen analysis is feasible.

### B. Forecast research

Deliver a reproducible dataset, baseline predictions, model predictions, chronological metrics, and a complete experiment log. Accept only if a reviewer can identify exactly what information each historical prediction used. Retrospective-only results must be labeled separately.

### C. Valuation research

Deliver operating projections, bear/base/bull cases, simulation summaries, sensitivities, and a price-implied expectations analysis. Accept only when assumptions reconcile to source data and all cash/share/earnings definitions are explicit.

### D. Thesis assessment

Deliver supporting and contrary evidence, catalysts, failure conditions, limitations, and a long/short/no-conviction research decision. Accept only if the conclusion follows from the evidence rather than a preselected position.

### E. Team-authored competition materials

Separate from AI-authored research artifacts, the team must prepare the required memo, Excel model, participant information, and resumes under the competition's authorship rules. A proposed independently built workbook structure is Sources, Historicals, Assumptions, Forecast, Valuation, Scenarios, and Checks. Formulas must be inspectable and imported research outputs clearly identified; final use depends on organizer clarification noted above.

For the research repository, save outputs under `outputs/<run_id>/`, including `run-manifest.json`, `forecast-predictions.csv`, `forecast-metrics.json`, `valuation-scenarios.csv`, `simulation-summary.json`, and labeled figures. These files remain ignored by Git unless a specific small, non-sensitive artifact is intentionally selected for versioning.

## 14. Milestones to the first-round deadline

### September 21-22: feasibility and scope lock

- Resolve registration status and rules questions.
- Confirm available team time and assign owners.
- Audit company target history, weather release timing, and industry data.
- Choose the target and freeze the initial model comparison protocol.
- Go/no-go: abandon the weather extension if it cannot support a credible test.

### September 23-24: dataset and baseline

- Build/reconcile quarterly fundamentals and source metadata.
- Implement fiscal aggregation and availability controls.
- Produce the first baseline backtest and operating bridge.

### September 25-26: independent evidence

- Evaluate the weather feature only if the feasibility gate passed.
- Compare a small regression with the baseline.
- Complete customer/competition evidence review.
- Cut optional ML if data or incremental performance are inadequate.

### September 27-28: valuation and uncertainty

- Complete deterministic cases and market-implied expectations.
- Add calibrated or clearly judgmental simulation assumptions.
- Reconcile material cash deployment, transactions, and share changes.

### September 29: challenge the thesis

- Have a team member argue the opposing position.
- Check whether the signal survives alternative assumptions and exclusions.
- Decide long, short, or insufficient evidence.
- If insufficient evidence, escalate immediately; do not conceal uncertainty to meet the schedule.

### September 30-October 1: team preparation and verification

- Freeze a cited data snapshot and reproduce the research run.
- Team independently prepares permitted submission materials.
- Audit page count, workbook formulas, sources, required resumes, and consistency of assumptions.

### October 2: final check and submission buffer

- Target team submission by 5 p.m. Pacific, before the official 8:59:59 p.m. Pacific equivalent of 11:59:59 p.m. Eastern.
- Confirm current organizer instructions and successful receipt.
- Submission is a team action; this scope does not authorize automated submission.

## 15. Team roles

Assign named owners before implementation:

- Research lead: thesis, competitive evidence, contrary evidence, catalysts, rules/registration.
- Data/modeling lead: source audit, dataset, forecasting, leakage controls, reproducibility.
- Valuation lead: accounting reconciliation, operating bridge, valuation, scenario logic.
- Reviewer/presenter: independent challenge, citation audit, material consistency, rehearsal.

For a two-person team, combine research with valuation and modeling with review, but cross-review each other's calculations. For three people, combine reviewer duties across the team. No person should be the sole reviewer of their own central assumption.

## 16. Stop, simplify, and pivot criteria

- No usable historical target: use a simpler disclosed metric or reconsider CPRT.
- Unavailable historical release vintages: separate retrospective association from forecasting evidence.
- Weather adds no robust predictive value: remove it from the central thesis.
- ML fails the comparison gate: retain the baseline/regression.
- Valuation depends almost entirely on an unsupported multiple expansion: reduce conviction or reject the position.
- The case requires an undisclosed customer recovery assumption: expose it as a scenario, not a modeled fact.
- No identifiable catalyst within 12 months: do not rely on a vague eventual rerating.
- Assumptions cannot explain a disagreement with the current price: conclude insufficient evidence.
- Core deliverables slip: remove GPU work, nonlinear ML, extra plots, and secondary valuation methods before weakening source or accounting checks.

## 17. Final completion checklist

- [ ] Participation and permitted use of research assistance resolved by the team.
- [ ] Public source provenance and information cutoff documented.
- [ ] Company history reconciled; missing values and definition changes visible.
- [ ] Forecast target and evaluation protocol fixed before final testing.
- [ ] Baseline and all attempted model results retained.
- [ ] Future information excluded or retrospective limitations explicitly labeled.
- [ ] Weather and regional exposure assumptions tested or removed.
- [ ] Operating forecasts reconcile with valuation inputs.
- [ ] Simulation distributions and dependencies explained; convergence checked.
- [ ] Price-implied expectations assessed without invented consensus.
- [ ] Contrary evidence, catalysts, and thesis failure conditions documented.
- [ ] A second team member has challenged material assumptions.
- [ ] Research run reproducible from frozen inputs and recorded environment.
- [ ] Team-authored materials independently checked against competition rules.

## 18. Current unresolved decisions

1. Was the team registered by September 18, or has an organizer exception been granted?
2. Who are the team members, and how many hours can each commit before October 2?
3. What organizer clarification applies to AI-assisted code and derived outputs?
4. Is a consistent historical U.S. service-volume series available, or must the target be revenue?
5. Are point-in-time industry and weather data adequate for the proposed backtest?
6. What exact GPU and VRAM are available? This does not block the CPU scope.
7. Which timestamped price and information cutoff will anchor the final research valuation?

The next implementation step is the data feasibility audit, not training a complex model.
