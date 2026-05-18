import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()


def generate_ai_explanation(health_data: dict, analysis: dict):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "AI explanation skipped because GEMINI_API_KEY is not configured."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an experienced SRE incident commander.

Analyze the following service health data and rule-based incident analysis.

Service health data:
{json.dumps(health_data, indent=2)}

Rule-based analysis:
{json.dumps(analysis, indent=2)}

Generate a concise incident explanation with these sections:
1. What is happening
2. Why this is likely happening
3. Immediate next actions
4. Leadership update

Keep it practical, calm, and SRE-focused.
Do not invent facts that are not present in the data.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        return response.text

    except Exception as error:
        return f"AI explanation failed: {error}"