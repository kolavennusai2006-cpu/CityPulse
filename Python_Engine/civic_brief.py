import os
from google import genai


def generate_civic_brief(evidence):
    """
    Generate a short, grounded civic brief from structured evidence.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "success": False,
            "brief": "Gemini API key is not configured."
        }

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are CityPulse, an AI system that explains civic conditions
to city staff and residents.

Use ONLY the structured evidence provided below.

Write a short civic brief explaining:
1. What is happening?
2. Which signals support it?
3. What stage is the event in?
4. What does the evidence suggest?
5. Do not claim causation when the data only shows correlation.

Rules:
- Do not invent information.
- Do not mention individuals.
- Keep it to 3-5 sentences.
- Use plain, professional language.
- Clearly distinguish observed evidence from possible relationships.
- If recovery is occurring, mention that the signals are decreasing.
- Do not make unsupported predictions.

STRUCTURED EVIDENCE:
{evidence}
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return {
            "success": True,
            "brief": interaction.output_text.strip()
        }

    except Exception as e:
        return {
            "success": False,
            "brief": "Unable to generate civic brief.",
            "error": str(e)
        }


if __name__ == "__main__":

    test_evidence = {
        "zone_id": "ZONE_A",
        "status": "CRITICAL",
        "risk_score": 100,
        "signals_detected": [
            "HEAVY_RAIN",
            "TRAFFIC_SPIKE",
            "TRANSIT_DELAY",
            "COMPLAINT_SPIKE"
        ],
        "event_stage": "RECOVERY",
        "recovery_level": "HIGH",
        "interpretation": (
            "Multiple civic signals changed significantly within "
            "the same time window. These signals show a possible "
            "relationship. This does not confirm causation."
        )
    }

    result = generate_civic_brief(test_evidence)

    print("CIVIC BRIEF TEST")
    print("=" * 50)
    print("Success:", result["success"])
    print()
    print("Brief:")
    print(result["brief"])

    if "error" in result:
        print()
        print("Error:")
        print(result["error"])