import pandas as pd


REQUIRED_CURVES = [
    "GR",
    "RT",
    "RHOB",
    "NPHI",
]


def assess_data_quality(
    df: pd.DataFrame,
) -> dict:

    total = len(df)

    available = []
    missing = []
    quality = {}

    for curve in REQUIRED_CURVES:

        if curve in df.columns:

            available.append(curve)

            missing_values = int(
                df[curve].isna().sum()
            )

            completeness = (
                1 - missing_values / total
            ) * 100

            quality[curve] = round(
                completeness,
                1,
            )

        else:

            missing.append(curve)

            quality[curve] = 0.0


    overall = (
        sum(quality.values())
        / len(quality)
    )


    if overall >= 90:
        status = "excellent"

    elif overall >= 75:
        status = "good"

    elif overall >= 50:
        status = "limited"

    else:
        status = "poor"


    return {
        "status": status,
        "score": round(overall, 1),
        "available_curves": available,
        "missing_curves": missing,
        "curve_completeness": quality,
        "sample_count": total,
    }