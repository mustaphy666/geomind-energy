from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_formation_pdf(report: dict) -> BytesIO:

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=10,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=14,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
    )

    story = []

    # ---------------------------------------
    # TITLE
    # ---------------------------------------

    story.append(
        Paragraph(
            "GEOMIND ENERGY",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Formation Evaluation Report",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            f"Well: {report.get('well_id', 'Unknown')}",
            body_style,
        )
    )

    story.append(
        Paragraph(
            f"Generated: {report.get('generated_at', '')}",
            small_style,
        )
    )

    story.append(Spacer(1, 15))

    # ---------------------------------------
    # DATA QUALITY
    # ---------------------------------------

    story.append(
        Paragraph(
            "1. Data Quality",
            heading_style,
        )
    )

    quality = report.get(
        "data_quality",
        {},
    )

    quality_data = [
        ["Metric", "Result"],
        [
            "Quality Score",
            f"{quality.get('score', 0)}/100",
        ],
        [
            "Status",
            str(
                quality.get(
                    "status",
                    "Unknown",
                )
            ).title(),
        ],
        [
            "Samples",
            str(
                quality.get(
                    "sample_count",
                    0,
                )
            ),
        ],
    ]

    quality_table = Table(
        quality_data,
        colWidths=[2.5 * inch, 2.5 * inch],
    )

    quality_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1f2937"),
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey,
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6,
            ),
        ])
    )

    story.append(quality_table)

    # ---------------------------------------
    # BEST RESERVOIR
    # ---------------------------------------

    best = report.get(
        "best_reservoir"
    )

    if best:

        story.append(
            Paragraph(
                "2. Best Candidate Reservoir",
                heading_style,
            )
        )

        best_data = [
            ["Property", "Value"],
            [
                "Interval",
                f"{best.get('top')} - "
                f"{best.get('base')} ft",
            ],
            [
                "Gross Thickness",
                f"{best.get('gross_thickness')} ft",
            ],
            [
                "Quality Score",
                f"{best.get('quality_score')}/100",
            ],
            [
                "Rank",
                f"#{best.get('quality_rank')}",
            ],
        ]

        best_table = Table(
            best_data,
            colWidths=[
                2.5 * inch,
                2.5 * inch,
            ],
        )

        best_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f2937"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ])
        )

        story.append(best_table)

    # ---------------------------------------
    # RESERVOIR ZONES
    # ---------------------------------------

    story.append(
        Paragraph(
            "3. Reservoir Zonation",
            heading_style,
        )
    )

    zone_rows = [
        [
            "Zone",
            "Top",
            "Base",
            "Thickness",
            "Classification",
        ]
    ]

    for zone in report.get(
        "zones",
        [],
    ):

        zone_rows.append([
            f"Zone {zone.get('zone')}",
            f"{zone.get('top')} ft",
            f"{zone.get('base')} ft",
            f"{zone.get('thickness')} ft",
            zone.get(
                "classification",
                "",
            ).replace(
                "_",
                " ",
            ),
        ])

    zone_table = Table(
        zone_rows,
        repeatRows=1,
        colWidths=[
            0.7 * inch,
            0.8 * inch,
            0.8 * inch,
            1.0 * inch,
            2.0 * inch,
        ],
    )

    zone_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1f2937"),
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey,
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8,
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                5,
            ),
        ])
    )

    story.append(zone_table)

    # ---------------------------------------
    # PAY INTERVALS
    # ---------------------------------------

    story.append(
        Paragraph(
            "4. Potential Pay Intervals",
            heading_style,
        )
    )

    pay_intervals = report.get(
        "pay_intervals",
        [],
    )

    if pay_intervals:

        pay_rows = [
            [
                "Top",
                "Base",
                "Thickness",
                "Vsh",
                "Porosity",
                "Sw",
            ]
        ]

        for interval in pay_intervals:

            pay_rows.append([
                str(interval.get("top")),
                str(interval.get("base")),
                str(
                    interval.get(
                        "gross_thickness",
                        "",
                    )
                ),
                f"{float(interval.get('average_vsh', 0)) * 100:.1f}%",
                f"{float(interval.get('average_porosity', 0)) * 100:.1f}%",
                f"{float(interval.get('average_sw', 0)) * 100:.1f}%",
            ])

        pay_table = Table(
            pay_rows,
            repeatRows=1,
        )

        pay_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f2937"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ])
        )

        story.append(pay_table)

    else:

        story.append(
            Paragraph(
                "No potential pay intervals were identified.",
                body_style,
            )
        )

    # ---------------------------------------
    # AI INTERPRETATION
    # ---------------------------------------

    story.append(
        Paragraph(
            "5. AI Formation Evaluation",
            heading_style,
        )
    )

    interpretation = report.get(
        "zone_interpretation",
        "",
    )

    story.append(
        Paragraph(
            interpretation.replace(
                "\n",
                "<br/>",
            ),
            body_style,
        )
    )

    # ---------------------------------------
    # DISCLAIMER
    # ---------------------------------------

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            report.get(
                "disclaimer",
                "",
            ),
            small_style,
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer