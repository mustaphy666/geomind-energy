from typing import Any


def build_formation_summary(
    dataframe,
    well_name: str | None = None,
) -> dict[str, Any]:

    df = dataframe.copy()

    summary = {
        "well_name": well_name,

        "depth_start": float(
            df["DEPTH"].min()
        ),

        "depth_end": float(
            df["DEPTH"].max()
        ),

        "samples": len(df),

        "average_vsh": float(
            df["VSH"].mean()
        ),

        "average_porosity": float(
            df["POROSITY"].mean()
        ),

        "average_sw": float(
            df["SW"].mean()
        ),

        "pay_samples": int(
            df["PAY"].sum()
        ),
    }


    # Calculate approximate pay interval
    pay_df = df[df["PAY"] == True]

    if len(pay_df) > 0:

        summary["pay_start"] = float(
            pay_df["DEPTH"].min()
        )

        summary["pay_end"] = float(
            pay_df["DEPTH"].max()
        )

        summary["pay_thickness"] = (
            summary["pay_end"]
            - summary["pay_start"]
        )

    else:

        summary["pay_start"] = None
        summary["pay_end"] = None
        summary["pay_thickness"] = 0.0


    return summary