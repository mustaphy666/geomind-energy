import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.welllog_service import (
    load_las_file,
    get_well_metadata,
    get_curve_information,
)


router = APIRouter(
    prefix="/welllogs",
    tags=["Well Logs"],
)


UPLOAD_DIR = "well_logs"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload")
async def upload_las(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".las"):
        raise HTTPException(
            status_code=400,
            detail="Only LAS files are supported."
        )

    well_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{well_id}.las"
    )

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    try:

        las = load_las_file(file_path)

        metadata = get_well_metadata(las)

        curves = get_curve_information(las)

    except Exception as error:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=f"Could not process LAS file: {error}"
        )

    return {
        "well_id": well_id,
        "filename": file.filename,
        "metadata": metadata,
        "curves": curves,
    }