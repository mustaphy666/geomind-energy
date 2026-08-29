import pandas as pd


def calculate_reservoir_quality(
    df: pd.DataFrame,
) -> pd.DataFrame:

    data = df.copy()

    # ------------------------------------------------
    # Normalize individual properties to 0–100
    # ------------------------------------------------

    # Porosity
    porosity_score = (
        data["POROSITY"]
        .clip(0, 0.30)
        / 0.30
        * 100
    )

    # Lower water saturation = better
    sw_score = (
        (1 - data["SW"])
        .clip(0, 1)
        * 100
    )

    # Lower shale volume = better
    vsh_score = (
        (1 - data["VSH"])
        .clip(0, 1)
        * 100
    )

    # ------------------------------------------------
    # Weighted score
    # ------------------------------------------------

    data["RQS"] = (
        porosity_score * 0.35
        + sw_score * 0.30
        + vsh_score * 0.25
        + 10
    )

    # Keep score between 0 and 100

    data["RQS"] = (
        data["RQS"]
        .clip(0, 100)
        .round(2)
    )

    return data
def score_intervals(
    intervals: list[dict],
) -> list[dict]:

    if not intervals:
        return []

    scored = []

    max_thickness = max(
        interval["gross_thickness"]
        for interval in intervals
    )

    for interval in intervals:

        porosity_score = (
            min(
                interval["average_porosity"],
                0.30,
            )
            / 0.30
            * 100
        )

        sw_score = (
            (1 - interval["average_sw"])
            * 100
        )

        vsh_score = (
            (1 - interval["average_vsh"])
            * 100
        )

        thickness_score = (
            interval["gross_thickness"]
            / max_thickness
            * 100
        )


        score = (
            porosity_score * 0.35
            + sw_score * 0.30
            + vsh_score * 0.25
            + thickness_score * 0.10
        )


        interval_copy = interval.copy()

        interval_copy["quality_score"] = round(
            max(
                0,
                min(score, 100)
            ),
            1,
        )

        scored.append(
            interval_copy
        )


    scored.sort(
        key=lambda x:
        x["quality_score"],
        reverse=True,
    )


    for rank, interval in enumerate(
        scored,
        start=1,
    ):

        interval[
            "quality_rank"
        ] = rank


    return scored