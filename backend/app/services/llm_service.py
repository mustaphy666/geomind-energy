import logging
import os
from dotenv import load_dotenv
from google import genai

from app.services.zone_ai_service import (
    build_zone_prompt,
)

load_dotenv()
logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=api_key)

    async def interpret_formation(self, summary: dict) -> str:
        prompt = f"""
You are GeoMind Energy, an AI copilot for petroleum geoscience and petrophysics.

You are assisting a petroleum geoscientist in the interpretation of
calculated well-log petrophysical results.

Your task is to transform the calculated formation-evaluation results
provided below into a concise, professional technical interpretation
written in the style of a petroleum geoscientist.

IMPORTANT DATA RULES:

- Use ONLY the calculated information provided in the Formation Evaluation data.
- Do not invent measurements, formations, lithologies, fluid contacts,
  reservoir pressures, fluid properties, or geological information.
- Do not claim that hydrocarbons have been confirmed.
- Do not infer information that cannot reasonably be supported by the
  calculated results.
- If an important parameter is unavailable, explicitly state that it
  cannot be assessed from the available data.
- Distinguish clearly between calculated results and geological/petrophysical
  interpretation.
- Treat pay intervals as candidate intervals identified by the applied
  petrophysical criteria, not as confirmed hydrocarbon-bearing zones.

WRITING STYLE:

Write like an experienced petroleum geoscientist preparing a short
formation-evaluation report for another technical professional.

The interpretation must:

- Be analytical rather than conversational.
- Use clear technical language.
- Avoid exaggerated claims.
- Avoid generic AI phrases such as "overall, the results indicate" when
  they add no useful information.
- Do not repeat the same conclusion in different sections.
- Do not restate every numerical value already provided in the tables.
- Refer to important values selectively when they support an interpretation.
- Use complete paragraphs rather than a list of disconnected observations.
- Do NOT use bullet points for the main interpretation.
- Do NOT use numbered lists.
- Do NOT use excessive headings.
- Do NOT use "•" bullets.
- Do NOT use ellipses such as "..." unless they are part of a quoted value.
- Keep the interpretation compact and information-dense.

STRUCTURE:

Write the interpretation using exactly these sections:

### Formation Evaluation

Provide a short opening assessment of the interpreted interval,
focusing on the general reservoir character revealed by the calculated
petrophysical properties.

### Petrophysical Interpretation

Discuss the reservoir quality by integrating shale volume, porosity,
and water saturation. Explain what the calculated values imply about
the quality and cleanliness of the reservoir interval. Do not discuss
each parameter as an isolated checklist item; integrate them into a
coherent interpretation.

### Pay Assessment

Discuss the identified candidate pay interval(s). Explain why the
interval qualifies as a candidate based on the calculated
petrophysical criteria. Clearly state that the interval represents a
petrophysical candidate and does not constitute confirmation of
hydrocarbon saturation or commercial producibility.

### Uncertainty and Limitations

Briefly discuss the most important uncertainties that affect the
interpretation. Mention only uncertainties that are relevant to the
available data and calculations.

### Recommended Evaluation

End with a short paragraph describing the most useful next steps for
validating the interpretation. Recommendations should be technically
relevant to formation evaluation, such as additional well-log
interpretation, core data, pressure information, fluid sampling,
formation testing, or other supporting data where appropriate.

IMPORTANT:

The final response should read like a professional technical report,
not an AI answer.

Do not create a long list of observations.

Do not repeat the input data unnecessarily.

Do not provide a generic explanation of petrophysics.

Focus specifically on what the calculated results mean for this
formation evaluation.

Formation Evaluation Data:

{summary}
"""
        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            logger.error(f"Error in interpret_formation: {e}")
            return (
                "AI formation evaluation is currently unavailable due to a network or connection issue. "
                "Please verify your GEMINI_API_KEY, internet connection, and try again."
            )

    async def interpret_zones(
        self,
        zones: list,
        pay_intervals: list,
        well_name: str | None = None,
    ) -> str:
        prompt = build_zone_prompt(
            zones=zones,
            pay_intervals=pay_intervals,
            well_name=well_name,
        )

        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            logger.error(f"Error in interpret_zones: {e}")
            return (
                "AI zone interpretation is currently unavailable. "
                "Please check system logs and network connectivity."
            )


llm_service = LLMService()

# import os
# import logging
# from dotenv import load_dotenv
# from groq import AsyncGroq

# from app.services.zone_ai_service import build_zone_prompt

# load_dotenv()
# logger = logging.getLogger(__name__)


# class LLMService:

#     def __init__(self):
#         api_key = os.getenv("GROQ_API_KEY")
#         if not api_key:
#             raise ValueError("GROQ_API_KEY is not configured in .env file.")

#         self.client = AsyncGroq(api_key=api_key)
#         # Using Llama 3.3 70B (fast and highly capable for technical summaries)
#         self.model = "openai/gpt-oss-120b"

#     async def interpret_formation(self, summary: dict) -> str:
#         prompt = f"""
#  You are GeoMind Energy, an AI copilot for petroleum geoscience and petrophysics.

# You are assisting a petroleum geoscientist in the interpretation of
# calculated well-log petrophysical results.

# Your task is to transform the calculated formation-evaluation results
# provided below into a concise, professional technical interpretation
# written in the style of a petroleum geoscientist.

#  IMPORTANT DATA RULES:

# - Use ONLY the calculated information provided in the Formation Evaluation data.
# - Do not invent measurements, formations, lithologies, fluid contacts,
#   reservoir pressures, fluid properties, or geological information.
# - Do not claim that hydrocarbons have been confirmed.
# - Do not infer information that cannot reasonably be supported by the
#   calculated results.
# - If an important parameter is unavailable, explicitly state that it
#   cannot be assessed from the available data.
# - Distinguish clearly between calculated results and geological/petrophysical
#   interpretation.
# - Treat pay intervals as candidate intervals identified by the applied
#   petrophysical criteria, not as confirmed hydrocarbon-bearing zones.

# WRITING STYLE:

# Write like an experienced petroleum geoscientist preparing a short
# formation-evaluation report for another technical professional.

# The interpretation must:

# - Be analytical rather than conversational.
# - Use clear technical language.
# - Avoid exaggerated claims.
# - Avoid generic AI phrases such as "overall, the results indicate" when
#   they add no useful information.
# - Do not repeat the same conclusion in different sections.
# - Do not restate every numerical value already provided in the tables.
# - Refer to important values selectively when they support an interpretation.
# - Use complete paragraphs rather than a list of disconnected observations.
# - Do NOT use bullet points for the main interpretation.
# - Do NOT use numbered lists.
# - Do NOT use excessive headings.
# - Do NOT use "•" bullets.
# - Do NOT use ellipses such as "..." unless they are part of a quoted value.
# - Keep the interpretation compact and information-dense.

# STRUCTURE:

# Write the interpretation using exactly these sections:

# ### Formation Evaluation

# Provide a short opening assessment of the interpreted interval,
# focusing on the general reservoir character revealed by the calculated
# petrophysical properties.

# ### Petrophysical Interpretation

# Discuss the reservoir quality by integrating shale volume, porosity,
# and water saturation. Explain what the calculated values imply about
# the quality and cleanliness of the reservoir interval. Do not discuss
# each parameter as an isolated checklist item; integrate them into a
# coherent interpretation.

# ### Pay Assessment

# Discuss the identified candidate pay interval(s). Explain why the
# interval qualifies as a candidate based on the calculated
# petrophysical criteria. Clearly state that the interval represents a
# petrophysical candidate and does not constitute confirmation of
# hydrocarbon saturation or commercial producibility.

# ### Uncertainty and Limitations

# Briefly discuss the most important uncertainties that affect the
# interpretation. Mention only uncertainties that are relevant to the
# available data and calculations.

# ### Recommended Evaluation

# End with a short paragraph describing the most useful next steps for
# validating the interpretation. Recommendations should be technically
# relevant to formation evaluation, such as additional well-log
# interpretation, core data, pressure information, fluid sampling,
# formation testing, or other supporting data where appropriate.

# IMPORTANT:

# The final response should read like a professional technical report,
# not an AI answer.

# Do not create a long list of observations.

# Do not repeat the input data unnecessarily.

# Do not provide a generic explanation of petrophysics.

# Focus specifically on what the calculated results mean for this
# formation evaluation.

# Formation Evaluation Data:

# {summary}
# """
#         try:
#             response = await self.client.chat.completions.create(
#                 messages=[{"role": "user", "content": prompt}],
#                 model=self.model,
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             logger.error(f"Groq API Error in interpret_formation: {e}")
#             return "AI formation evaluation unavailable. Please check backend logs."

#     async def interpret_zones(
#         self,
#         zones: list,
#         pay_intervals: list,
#         well_name: str | None = None,
#     ) -> str:
#         prompt = build_zone_prompt(
#             zones=zones,
#             pay_intervals=pay_intervals,
#             well_name=well_name,
#         )

#         try:
#             response = await self.client.chat.completions.create(
#                 messages=[{"role": "user", "content": prompt}],
#                 model=self.model,
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             logger.error(f"Groq API Error in interpret_zones: {e}")
#             return "AI zone interpretation unavailable. Please check backend logs."


# llm_service = LLMService()