import pandas as pd


def classify_zones(
    df: pd.DataFrame,
    max_vsh: float = 0.45,
    min_porosity: float = 0.10,
) -> list[dict]:

    data = df.copy()

    data = data.sort_values(
        "DEPTH"
    ).reset_index(drop=True)

    data["RESERVOIR"] = (
        (data["VSH"] <= max_vsh)
        &
        (data["POROSITY"] >= min_porosity)
    )

    zones = []

    start = 0
    current_status = bool(
        data.loc[0, "RESERVOIR"]
    )

    for i in range(1, len(data)):

        status = bool(
            data.loc[i, "RESERVOIR"]
        )

        if status != current_status:

            zone = _create_zone(
                data,
                start,
                i - 1,
                current_status,
            )

            zones.append(zone)

            start = i
            current_status = status

    # Final zone

    zone = _create_zone(
        data,
        start,
        len(data) - 1,
        current_status,
    )

    zones.append(zone)

    # Number zones

    for i, zone in enumerate(
        zones,
        start=1,
    ):
        zone["zone"] = i

    return zones


def _create_zone(
    df: pd.DataFrame,
    start: int,
    end: int,
    is_reservoir: bool,
) -> dict:

    zone = df.iloc[
        start:end + 1
    ]

    top = float(
        zone["DEPTH"].iloc[0]
    )

    base = float(
        zone["DEPTH"].iloc[-1]
    )

    if len(zone) > 1:

        step = float(
            zone["DEPTH"].diff().median()
        )

    else:

        step = 0.0

    thickness = (
        base - top + step
    )

    return {
        "top": round(top, 2),

        "base": round(base, 2),

        "thickness": round(
            thickness,
            2,
        ),

        "classification": (
            "candidate_reservoir"
            if is_reservoir
            else "non_reservoir"
        ),

        "average_vsh": round(
            float(
                zone["VSH"].mean()
            ),
            4,
        ),

        "average_porosity": round(
            float(
                zone["POROSITY"].mean()
            ),
            4,
        ),

        "average_sw": round(
            float(
                zone["SW"].mean()
            ),
            4,
        ),

        "samples": len(zone),
    }