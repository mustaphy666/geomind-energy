from datetime import datetime
from typing import Any


def build_formation_report(
    well_id: str,
    summary: dict[str, Any],
    data_quality: dict[str, Any],
    zones: list[dict[str, Any]],
    reservoir_quality: list[dict[str, Any]],
    pay_intervals: list[dict[str, Any]],
    interpretation: str,
    zone_interpretation: str,
) -> dict[str, Any]:

    # -----------------------------------------
    # Find highest-ranked reservoir
    # -----------------------------------------

    best_reservoir = None

    if reservoir_quality:

        best_reservoir = max(
            reservoir_quality,
            key=lambda x: x.get(
                "quality_score",
                0,
            ),
        )

    # -----------------------------------------
    # Build report
    # -----------------------------------------

    report = {

        "report_title":
            "GeoMind Energy Formation Evaluation",

        "generated_at":
            datetime.utcnow().isoformat(),

        "well_id":
            well_id,

        "data_quality":
            data_quality,

        "formation_summary":
            summary,

        "zones":
            zones,

        "reservoir_quality":
            reservoir_quality,

        "pay_intervals":
            pay_intervals,

        "best_reservoir":
            best_reservoir,

        "overall_interpretation":
            interpretation,

        "zone_interpretation":
            zone_interpretation,

        "disclaimer":
            (
                "AI-assisted interpretation based "
                "on calculated well-log properties. "
                "Results should be independently "
                "reviewed by a qualified "
                "petrophysicist or petroleum "
                "geoscientist before operational "
                "decisions."
            ),
    }

    return report