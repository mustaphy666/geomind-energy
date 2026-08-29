from pathlib import Path

import lasio
import pandas as pd


def load_las_file(file_path: str) -> lasio.LASFile:
    """
    Load a LAS well-log file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"LAS file not found: {file_path}"
        )

    if path.suffix.lower() != ".las":
        raise ValueError(
            "Only LAS files are supported."
        )

    return lasio.read(file_path)


def get_well_metadata(las: lasio.LASFile) -> dict:
    """
    Extract basic metadata from a LAS file.
    """

    well = las.well

    return {
        "well_name": str(well.WELL.value)
        if "WELL" in well
        else None,

        "field": str(well.FLD.value)
        if "FLD" in well
        else None,

        "company": str(well.COMP.value)
        if "COMP" in well
        else None,

        "start_depth": float(las.index.min()),

        "end_depth": float(las.index.max()),

        "curve_count": len(las.curves),
    }


def get_curve_information(
    las: lasio.LASFile
) -> list[dict]:
    """
    Return information about every curve
    contained in the LAS file.
    """

    curves = []

    for curve in las.curves:

        curves.append(
            {
                "mnemonic": curve.mnemonic,
                "unit": curve.unit,
                "description": curve.descr,
            }
        )

    return curves


def las_to_dataframe(
    las: lasio.LASFile
) -> pd.DataFrame:
    """
    Convert LAS curves to a pandas DataFrame.
    """

    dataframe = las.df()

    dataframe.reset_index(inplace=True)

    return dataframe