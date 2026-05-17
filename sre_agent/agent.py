import sys
import os
import json
from dotenv import load_dotenv
from google import genai
from sre_agent.tools.monitoring_tools import get_service_health
from sre_agent.analysis.incident_analyzer import build_incident_analysis


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


def format_report(analysis: dict, ai_explanation: str):
    evidence = analysis["evidence"]

    return f"""
================ SRE INCIDENT TRIAGE REPORT ================

Service: {analysis["service"]}
Status: {analysis["status"].upper()}
Severity: {analysis["severity"]}

Evidence:
- Availability: {evidence["availability"]}
- P95 latency: {evidence["latency_p95_ms"]} ms
- Error rate: {evidence["error_rate_percent"]}%
- Recent change: {evidence["recent_change"]}

Likely cause:
{analysis["likely_cause"]}

Recommended action:
{analysis["recommended_action"]}

Leadership summary:
{analysis["leadership_summary"]}

AI-generated incident explanation:
{ai_explanation}

============================================================
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sre_agent/agent.py <service_name>")
        print("Example: python sre_agent/agent.py checkout")
        sys.exit(1)

    service_name = sys.argv[1]

    health = get_service_health(service_name)
    analysis = build_incident_analysis(health)
    ai_explanation = generate_ai_explanation(health, analysis)

    print(format_report(analysis, ai_explanation))

    print("Structured JSON output:")
    print(json.dumps(analysis, indent=2))