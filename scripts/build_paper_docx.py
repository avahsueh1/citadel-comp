"""Create the editable research report with original Python-generated PNGs."""

from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


def build():
    root = Path(__file__).resolve().parents[1]
    output = root / "docs" / "copart-research-report.docx"
    figures = root / "docs" / "figures"
    images = [
        figures / "06-predictive-weather.png",
    ]
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = section.bottom_margin = Inches(0.6)
    section.left_margin = section.right_margin = Inches(0.7)
    section.footer_distance = Inches(0.25)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.02
    for name in ["Heading 1", "Heading 2"]:
        style = doc.styles[name]
        style.font.name = "Calibri"
        style.font.size = Pt(11)
        style.font.color.rgb = RGBColor.from_string("253F52")
        style.paragraph_format.space_before = Pt(8)
        style.paragraph_format.space_after = Pt(3)
    doc.styles["Title"].font.name = "Cambria"
    doc.styles["Title"].font.size = Pt(22)
    doc.styles["Title"].font.color.rgb = RGBColor(0, 0, 0)
    doc.styles["Title"].paragraph_format.space_after = Pt(5)

    def para(text, size=None, bold=False, color=None):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        return p

    def heading(text):
        doc.add_heading(text, level=1)

    doc.add_paragraph("Copart investment research report", "Title")
    para("CPRT  |  September 30, 2026  |  Research draft", 10, True)
    para("Recommendation: [Steven]   Horizon: [3–12 months]   Target: [after testing]", 10)
    para(
        "Not submission-ready. Rules allow disclosed initial AI research but prohibit "
        "generative-AI submission content, in whole or part. This includes more than "
        "prose; Python generation does not itself establish eligibility.",
        8,
        color="7F4B35",
    )

    heading("Investment thesis")
    para(
        "[Steven: State LONG or SHORT, the expectation the market has wrong, the "
        "evidence for a different outcome, and the catalyst that will reveal it within "
        "the investment horizon.]",
        color="895824",
    )
    para(
        "The research question is whether Copart’s operating slowdown reflects "
        "temporary conditions or a lasting change in growth and profitability. The "
        "separate Excel submission translates service revenue, vehicle sales, operating"
        " costs and reinvestment into cash flow and value. The recommendation remains "
        "open until the thesis assumptions are tested."
    )

    heading("Operating evidence and competition")
    para(
        "The supplied workbook records FY2026 revenue of $4,666.2 million, up 0.4%, and"
        " operating income of $1,652.6 million versus $1,696.7 million in FY2025. "
        "Operating margin falls from 36.5% to 35.4%. Service revenue is approximately "
        "flat at $3,969.5 million; purchased-vehicle revenue rises 2.7% to $696.7 "
        "million. FY2026 is labeled unaudited. These figures focus the thesis on "
        "growth, cost absorption and reinvestment. [1]"
    )
    para(
        "[Steven: Add a relevant industry overview, competitive strengths and "
        "weaknesses, customer-retention evidence, and management assessment. Cite "
        "public sources and address the strongest competing explanation.]",
        color="895824",
    )

    heading("Valuation and assumption testing")
    para(
        "The workbook forecasts FY2027–FY2031 free cash flow to the firm, discounts the"
        " explicit cash flows and terminal value, and bridges enterprise value to "
        "equity value. Its provisional inputs include 9.0% WACC, 2.5% terminal growth "
        "and approximately 0.02% annual service-revenue growth. The saved standalone "
        "value is $23.30 per share, 14.4% below the workbook’s $27.22 reference price "
        "labeled September 28, 2026. This is not a validated target or a short "
        "recommendation. [2]"
    )
    para(
        "Terminal value accounts for 73.1% of enterprise value. The cash/debt/share "
        "bridge remains provisional and the acquisition-adjusted value is blank. The "
        "paper should report tested bear/base/bull assumptions and distinguish present "
        "DCF value from the eventual price target. Excel will be submitted separately. "
        "[2]"
    )
    para(
        "[After testing: insert scenario values and returns, changed growth/cost "
        "assumptions, WACC sensitivity, verified reference price, and the rationale for"
        " the selected investment horizon.]",
        color="895824",
    )

    heading("Catalysts and risks")
    para(
        "[Steven: Add two dated catalysts, the operating metric each should reveal, and"
        " a clear thesis-invalidating observation.]",
        color="895824",
    )
    para(
        "Test persistent service-revenue weakness, higher costs and greater capital "
        "needs. The workbook excludes the pending ACV transaction from standalone "
        "value; any transaction case must incorporate both consideration paid and "
        "supported value received, including integration costs. If recommending a "
        "short, address borrow and squeeze risk. [2]"
    )
    para(
        "Sources: [1] CopartDCFValuationModeL.xlsx, Historical Data D6:E13; Forecast "
        "E37:E38. [2] Same workbook, Assumptions F6:J35; Forecast F43:J47; Valuation "
        "B5:B11, B20:B32, B37:B53. Values are saved workbook results, not a fresh Excel"
        " recalculation or independently verified market quote.",
        8,
    )

    doc.add_page_break()
    heading("Historical evidence and forward weather forecast")
    para(
        "Proposed Copart connection: damaging weather may increase insured total-loss "
        "vehicles, some of which may be assigned to Copart and subsequently sold. "
        "Assignment share, auction timing, fees and handling costs determine the "
        "financial effect. This is a hypothesis to test, not an estimated relationship.",
        9,
    )
    para(
        "Historical context: FY2025 flash-flood records exceeded the seasonal median in"
        " all four quarters, while hail and flood records were below median in three "
        "quarters. The forward forecast below estimates U.S. event-record counts for "
        "FY2027 Q2–Q4 as of September 30, 2026. It does not estimate Copart revenue or "
        "insured losses and is not weighted by vehicle exposure or Copart’s footprint.",
        9,
    )
    for image, width, caption, alt in [
        (
            images[0],
            7.0,
            "Figure 1. Forward forecasts with historical error ranges. Dots are "
            "forecasts; vertical whiskers show uncertainty estimated from "
            "development-period errors. Panel scales differ.",
            "Three panels forecast hail, flash-flood and flood records for FY2027 Q2 "
            "through Q4. Blue dots show point forecasts and vertical lines show "
            "historical error ranges. Seasonal median forecasts are selected for all "
            "categories.",
        ),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(1)
        shape = p.add_run().add_picture(str(image), width=Inches(width))
        shape._inline.docPr.set("descr", alt)
        para(caption, 8)
    heading("Methodology")
    para(
        "We compare a seasonal-median forecast with fixed-penalty ridge regression "
        "using seasonal indicators and a time trend. Each September forecast uses data "
        "only through the previous December, matching the current data gap. Model "
        "selection uses 21 predictions per category from September 2015–2021 origins. "
        "The September 2022 origin is excluded from selection to keep its outcomes out "
        "of the first holdout information set. September 2023 and 2024 origins provide "
        "six held-out quarters per category, spanning FY2024 and FY2025 Q2–Q4. Revised "
        "NOAA data prevent a true historical-vintage test.",
        9,
    )
    para(
        "The seasonal median wins model selection for all three categories. Held-out "
        "mean absolute errors are 307 hail records, 449 flash-flood records and 187 "
        "flood records, versus 1,297, 535 and 145 for ridge regression. Ridge improves "
        "the flood holdout result but was not selected using that holdout. Historical "
        "error ranges target 80% coverage; observed coverage is 100%, 67% and 100%, "
        "respectively, on only six tests each. Forward coverage is not guaranteed.",
        9,
    )
    heading("Implication for the investment thesis")
    para(
        "This adds a genuine forward weather component, but it does not establish "
        "predictive support for the stock recommendation. The evidence favors a "
        "seasonal weather baseline, not a demonstrated ML advantage or revenue uplift. "
        "Keep weather effects out of the base-case revenue forecast until lagged "
        "weather improves out-of-sample Copart forecasts. Test service revenue or "
        "assignments against a financial-only baseline, then translate supported "
        "changes through the separate Excel model’s costs, cash flows and valuation. "
        "Four annual financial observations cannot validate that relationship.",
        9,
    )
    para(
        "[Team completion: state the operating forecast, forecast period, evidence for "
        "the assumption, difference from a sourced market expectation, and resulting "
        "valuation/return. Without this financial link, the weather forecast alone is "
        "insufficient evidence for the investment thesis.]",
        8, color="895824",
    )
    para(
        "Source: NOAA Storm Events revised 2010–2025 snapshots, U.S. states/DC; "
        "ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/. Latest complete training "
        "quarter ends October 2025; no 2026 weather is used. Original Python PNG "
        "embedded. Reproducible forecast values and test results: "
        "docs/figures/06-weather-forecast.csv and 06-weather-forecast-report.json. "
        "Counts are records, not unique storms or losses.",
        8,
    )
    para(
        "Submission format: final team-authored memorandum must be PDF, at most two "
        "pages including any appendix, with a separate Excel valuation model. DOCX is "
        "an editing format. Pagination has not been verified. All sources must be cited"
        " and initial AI research disclosed to the sponsor.",
        8,
    )

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = footer.add_run()
    r.font.size = Pt(8)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r._r.addnext(fld)
    doc.core_properties.title = "Copart investment research report"
    doc.core_properties.subject = "Research draft with separate Excel model references"
    doc.core_properties.author = ""
    doc.save(output)
    with ZipFile(output) as archive:
        embedded = [
            sha256(archive.read(n)).hexdigest()
            for n in archive.namelist()
            if n.startswith("word/media/")
        ]
    assert sorted(embedded) == sorted(sha256(p.read_bytes()).hexdigest() for p in images)
    print(f"Created {output}; all embedded image hashes match the original Python PNGs.")


if __name__ == "__main__":
    build()
