import numpy as np
import pandas as pd


def calculate_vshale(
    gr: pd.Series,
    gr_clean: float,
    gr_shale: float,
) -> pd.Series:
    """
    Calculate shale volume using the Linear Gamma Ray method.
    """

    if gr_shale == gr_clean:
        raise ValueError(
            "Clean and shale GR values cannot be equal."
        )

    igr = (gr - gr_clean) / (
        gr_shale - gr_clean
    )

    vsh = igr.clip(0, 1)

    return vsh


def calculate_density_porosity(
    rhob: pd.Series,
    rho_matrix: float = 2.65,
    rho_fluid: float = 1.0,
) -> pd.Series:
    """
    Calculate density-derived porosity.

    phi = (rho_matrix - rho_bulk) /
          (rho_matrix - rho_fluid)
    """

    if rho_matrix <= rho_fluid:
        raise ValueError(
            "Matrix density must be greater than fluid density."
        )

    phi = (
        rho_matrix - rhob
    ) / (
        rho_matrix - rho_fluid
    )

    return phi.clip(0, 1)


def calculate_neutron_density_porosity(
    nphi: pd.Series,
    density_phi: pd.Series,
) -> pd.Series:
    """
    Simple neutron-density average.
    """

    phi = (
        nphi + density_phi
    ) / 2

    return phi.clip(0, 1)


def calculate_archie_sw(
    rt: pd.Series,
    porosity: pd.Series,
    rw: float,
    a: float = 1.0,
    m: float = 2.0,
    n: float = 2.0,
) -> pd.Series:
    """
    Calculate water saturation using Archie.

    Sw = [(a * Rw) /
          (phi^m * Rt)]^(1/n)
    """

    numerator = a * rw

    denominator = (
        porosity ** m
    ) * rt

    sw = (
        numerator / denominator
    ) ** (1 / n)

    return sw.clip(0, 1)


def identify_pay_zones(
    dataframe: pd.DataFrame,
    vsh_cutoff: float = 0.40,
    porosity_cutoff: float = 0.10,
    sw_cutoff: float = 0.60,
) -> pd.DataFrame:
    """
    Identify potential pay intervals.
    """

    dataframe = dataframe.copy()

    dataframe["PAY"] = (
        (dataframe["VSH"] <= vsh_cutoff)
        &
        (dataframe["POROSITY"] >= porosity_cutoff)
        &
        (dataframe["SW"] <= sw_cutoff)
    )

    return dataframe
def run_petrophysical_analysis(
    dataframe: pd.DataFrame,
    gr_clean: float = 20.0,
    gr_shale: float = 120.0,
    rho_matrix: float = 2.65,
    rho_fluid: float = 1.0,
    rw: float = 0.05,
    a: float = 1.0,
    m: float = 2.0,
    n: float = 2.0,
    vsh_cutoff: float = 0.40,
    porosity_cutoff: float = 0.10,
    sw_cutoff: float = 0.60,
) -> pd.DataFrame:

    df = dataframe.copy()

    required_curves = [
        "GR",
        "RHOB",
        "RT",
    ]

    missing = [
        curve
        for curve in required_curves
        if curve not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required curves: {missing}"
        )

    # -----------------------------
    # Vshale
    # -----------------------------

    df["VSH"] = calculate_vshale(
        df["GR"],
        gr_clean,
        gr_shale,
    )


    # -----------------------------
    # Density Porosity
    # -----------------------------

    df["DENSITY_POROSITY"] = (
        calculate_density_porosity(
            df["RHOB"],
            rho_matrix,
            rho_fluid,
        )
    )


    # -----------------------------
    # Porosity
    # -----------------------------

    if "NPHI" in df.columns:

        df["POROSITY"] = (
            calculate_neutron_density_porosity(
                df["NPHI"],
                df["DENSITY_POROSITY"],
            )
        )

    else:

        df["POROSITY"] = (
            df["DENSITY_POROSITY"]
        )


    # -----------------------------
    # Water Saturation
    # -----------------------------

    df["SW"] = calculate_archie_sw(
    df["RT"],
    df["POROSITY"],
    rw,
    a,
    m,
    n,
)

    # -----------------------------
    # Pay Zone
    # -----------------------------

    df = identify_pay_zones(
    df,
    vsh_cutoff=vsh_cutoff,
    porosity_cutoff=porosity_cutoff,
    sw_cutoff=sw_cutoff,
)

    return df