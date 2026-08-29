import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.welllog_service import (
    load_las_file,
    las_to_dataframe,
)
from app.services.zonation_service import (
    classify_zones,
)
from app.services.petrophysics_service import (
    run_petrophysical_analysis,
)
from app.services.formation_ai import (
    build_formation_summary,
)
from app.services.pay_zone_service import (
    detect_pay_intervals,
)
from app.services.pdf_service import (
    generate_formation_pdf,
)
from fastapi.responses import StreamingResponse
from app.services.llm_service import LLMService
from app.services.llm_service import (
    llm_service,
)
from app.services.reservoir_quality_service import (
    calculate_reservoir_quality,
    score_intervals,
)
from app.services.data_quality_service import (
    assess_data_quality,
)
from app.services.report_service import (
    build_formation_report,
)
llm_service = LLMService()
class PetrophysicsSettings(BaseModel):

    gr_clean: float = 20.0
    gr_shale: float = 120.0

    rho_matrix: float = 2.65
    rho_fluid: float = 1.0

    rw: float = 0.05

    a: float = 1.0
    m: float = 2.0
    n: float = 2.0

    vsh_cutoff: float = 0.40
    porosity_cutoff: float = 0.10
    sw_cutoff: float = 0.60
router = APIRouter(
    prefix="/petrophysics",
    tags=["Petrophysics"],
)


@router.post("/analyze/{well_id}")
async def analyze_well(
    well_id: str,
    settings: PetrophysicsSettings,
):

    file_path = f"well_logs/{well_id}.las"

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail="Well log not found."
        )

    try:

        las = load_las_file(
            file_path
        )

        dataframe = las_to_dataframe(
            las
        )
        quality_report = assess_data_quality(
    dataframe
)

        result = run_petrophysical_analysis(
            dataframe,

            gr_clean=settings.gr_clean,
            gr_shale=settings.gr_shale,

            rho_matrix=settings.rho_matrix,
            rho_fluid=settings.rho_fluid,

            rw=settings.rw,

            a=settings.a,
            m=settings.m,
            n=settings.n,

            vsh_cutoff=settings.vsh_cutoff,
            porosity_cutoff=settings.porosity_cutoff,
            sw_cutoff=settings.sw_cutoff,
        )
    
        result = calculate_reservoir_quality(
    result
)
        zones = classify_zones(
    result,

    max_vsh=0.45,

    min_porosity=0.10,
)
        pay_intervals = detect_pay_intervals(
    result,

    max_vsh=settings.vsh_cutoff,

    min_porosity=settings.porosity_cutoff,

    max_sw=settings.sw_cutoff,

    reservoir_max_vsh=0.45,

    reservoir_min_porosity=0.10,

    max_gap_samples=2,

    min_thickness=2.0
    )
        scored_reservoirs = score_intervals(
        pay_intervals["reservoir"]
    )   
        zone_interpretation = await llm_service.interpret_zones(
        zones=zones,
        pay_intervals=pay_intervals["pay"],
        well_name=well_id,
    )
        
        summary = build_formation_summary(
        result
        )   
        ai_interpretation = await llm_service.interpret_formation(
        summary
        )    
        report = build_formation_report(
    well_id=well_id,
    summary=summary,
    data_quality=quality_report,
    zones=zones,
    reservoir_quality=scored_reservoirs,
    pay_intervals=pay_intervals["pay"],
    interpretation=ai_interpretation,
    zone_interpretation=zone_interpretation,
)

        # Return a manageable response
        result = result.replace(
            [float("inf"), float("-inf")],
            None
        )

        result = result.fillna(None)

        return {
    "well_id": well_id,
    "data_quality": quality_report,

    "summary": summary,
    "zones": zones,

    "pay_intervals": pay_intervals,

    "reservoir_intervals": pay_intervals["reservoir"],
    "reservoir_quality":
        scored_reservoirs,
     "zone_interpretation":
        zone_interpretation,
    "interpretation": ai_interpretation,
    "report": report,
    "columns": list(result.columns),

    "data": result.to_dict(
        orient="records"
    ),
}
    except Exception as error:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
@router.post("/report/pdf")
async def download_report_pdf(
    report: dict,
):

    pdf_file = generate_formation_pdf(
        report
    )

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                "attachment; "
                "filename=GeoMind_Formation_Report.pdf"
        },
    )