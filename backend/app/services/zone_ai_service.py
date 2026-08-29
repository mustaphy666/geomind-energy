from typing import Any


def build_zone_prompt(
    zones: list[dict[str, Any]],
    pay_intervals: list[dict[str, Any]],
    well_name: str | None = None,
) -> str:

    zone_text = ""

    for zone in zones:

        zone_text += f"""
Zone {zone["zone"]}

Top: {zone["top"]} ft
Base: {zone["base"]} ft
Thickness: {zone["thickness"]} ft

Classification:
{zone["classification"]}

Average Vsh:
{zone["average_vsh"]}

Average Porosity:
{zone["average_porosity"]}

Average Water Saturation:
{zone["average_sw"]}

Samples:
{zone["samples"]}

"""


    pay_text = ""

    for interval in pay_intervals:

        pay_text += f"""
Potential Pay Interval

Top: {interval["top"]} ft
Base: {interval["base"]} ft
Gross Thickness: {interval["gross_thickness"]} ft

Average Vsh:
{interval["average_vsh"]}

Average Porosity:
{interval["average_porosity"]}

Average Water Saturation:
{interval["average_sw"]}

"""


    prompt = f"""
You are GeoMind Energy, an AI-assisted
petrophysical and formation-evaluation
copilot.

You are analyzing well-log-derived
petrophysical results.

Well:
{well_name or "Unknown"}

IMPORTANT:

Use ONLY the numerical information
provided below.

Do not invent log measurements.

Do not claim hydrocarbons are confirmed.

Do not present the interpretation as a
replacement for a qualified petrophysicist.

Evaluate each zone independently.

For each zone discuss:

1. Reservoir quality
2. Shale content
3. Porosity quality
4. Water saturation
5. Potential hydrocarbon significance
6. Confidence level
7. Main uncertainty

Then provide:

- Best candidate reservoir zone
- Best potential pay interval
- Overall formation evaluation
- Recommended next analysis

ZONE DATA:

{zone_text}

PAY INTERVAL DATA:

{pay_text}

Keep the interpretation technical,
concise and suitable for a petroleum
geoscience workflow.
"""

    return prompt