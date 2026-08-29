from typing import Any
import pandas as pd


def detect_pay_intervals(
    df: pd.DataFrame,
    max_vsh: float = 0.40,
    min_porosity: float = 0.10,
    max_sw: float = 0.60,

    # Broader reservoir criteria
    reservoir_max_vsh: float = 0.45,
    
    reservoir_min_porosity: float = 0.10,

    # Allow small non-reservoir gaps caused by log noise
    max_gap_samples: int = 2,

    # Minimum interval thickness in log units
    min_thickness: float = 2.0,
) -> list[dict[str, Any]]:

    data = df.copy()

    data = data.sort_values(
        "DEPTH"
    ).reset_index(drop=True)


    # --------------------------------------------------
    # 1. RESERVOIR FLAG
    # --------------------------------------------------

    data["IS_RESERVOIR"] = (
        (data["VSH"] <= reservoir_max_vsh)
        &
        (data["POROSITY"] >= reservoir_min_porosity)
    )


    # --------------------------------------------------
    # 2. PAY FLAG
    # --------------------------------------------------

    data["IS_PAY"] = (
        (data["VSH"] <= max_vsh)
        &
        (data["POROSITY"] >= min_porosity)
        &
        (data["SW"] <= max_sw)
    )


    # --------------------------------------------------
    # 3. BRIDGE SMALL GAPS
    # --------------------------------------------------

    data["RESERVOIR_GROUP"] = (
        data["IS_RESERVOIR"]
        .astype(int)
    )

    data["PAY_GROUP"] = (
        data["IS_PAY"]
        .astype(int)
    )


    data["RESERVOIR_GROUP"] = _bridge_gaps(
        data["RESERVOIR_GROUP"],
        max_gap_samples,
    )

    data["PAY_GROUP"] = _bridge_gaps(
        data["PAY_GROUP"],
        max_gap_samples,
    )


    # --------------------------------------------------
    # 4. BUILD RESERVOIR INTERVALS
    # --------------------------------------------------

    reservoir_intervals = _build_intervals(
        data,
        group_column="RESERVOIR_GROUP",
        flag_column="IS_RESERVOIR",
        min_thickness=min_thickness,
        interval_type="reservoir",
    )


    # --------------------------------------------------
    # 5. BUILD PAY INTERVALS
    # --------------------------------------------------

    pay_intervals = _build_intervals(
        data,
        group_column="PAY_GROUP",
        flag_column="IS_PAY",
        min_thickness=min_thickness,
        interval_type="pay",
    )


    # Rank by thickness

    reservoir_intervals = sorted(
        reservoir_intervals,
        key=lambda x: x["gross_thickness"],
        reverse=True,
    )

    pay_intervals = sorted(
        pay_intervals,
        key=lambda x: x["net_pay"],
        reverse=True,
    )


    for rank, interval in enumerate(
        reservoir_intervals,
        start=1,
    ):
        interval["rank"] = rank


    for rank, interval in enumerate(
        pay_intervals,
        start=1,
    ):
        interval["rank"] = rank


    return {
    "pay": pay_intervals,
    "reservoir": reservoir_intervals,
}


def _bridge_gaps(
    flags: pd.Series,
    max_gap_samples: int,
) -> pd.Series:

    result = flags.copy()
    values = result.to_numpy(copy=True)

    i = 0
    while i < len(values):

        if values[i] == 1:

            i += 1
            continue
        start = i
        while (
            i < len(values)
            and values[i] == 0
        ):
            i += 1
        end = i - 1

        gap_size = (
            end - start + 1
        )
        has_left = start > 0
        has_right = i < len(values)
        if (
            has_left
            and has_right
            and gap_size <= max_gap_samples
            and values[start - 1] == 1
            and values[i] == 1
        ):

            values[start:i] = 1


    return pd.Series(
        values,
        index=flags.index,
        name=flags.name,
    )


def _build_intervals(
    df: pd.DataFrame,
    group_column: str,
    flag_column: str,
    min_thickness: float,
    interval_type: str,
) -> list[dict[str, Any]]:

    intervals = []

    grouped = (
        df[df[flag_column]]
        .groupby(group_column)
    )


    for _, group in grouped:

        if group.empty:
            continue


        top = float(
            group["DEPTH"].min()
        )

        base = float(
            group["DEPTH"].max()
        )


        # Determine log sampling interval

        depth_values = (
            df["DEPTH"]
            .dropna()
            .sort_values()
            .unique()
        )


        if len(depth_values) > 1:

            step = float(
                pd.Series(
                    depth_values
                ).diff()
                .median()
            )

        else:
            step = 0.0


        gross_thickness = (
            base - top + step
        )


        if gross_thickness < min_thickness:
            continue


        result = {

            "type": interval_type,

            "top": round(
                top,
                2,
            ),

            "base": round(
                base,
                2,
            ),

            "gross_thickness": round(
                gross_thickness,
                2,
            ),

            "average_vsh": round(
                float(
                    group["VSH"].mean()
                ),
                4,
            ),

            "average_porosity": round(
                float(
                    group["POROSITY"].mean()
                ),
                4,
            ),

            "average_sw": round(
                float(
                    group["SW"].mean()
                ),
                4,
            ),

            "samples": int(
                len(group)
            ),
        }


        # For pay intervals,
        # estimate net pay from
        # qualifying samples.

        if interval_type == "pay":

            result["net_pay"] = round(
                len(group) * step,
                2,
            )

        else:

            result["net_pay"] = 0.0


        intervals.append(result)


    return intervals