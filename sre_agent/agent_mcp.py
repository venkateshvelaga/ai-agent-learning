import sys
import os
import json
import asyncio

from dotenv import load_dotenv
from google import genai

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from sre_agent.analysis.incident_analyzer import build_incident_analysis


load_dotenv()


async def get_service_health_via_mcp(service_name: str):
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sre_agent.mcp_server.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_service_health_tool",
                arguments={"service_name": service_name},
            )

            for content in result.content:
                if hasattr(content, "text"):
                    return json.loads(content.text)

    raise RuntimeError("No valid response received from MCP server.")


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

Execution mode: MCP-based agent

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


async def run_agent(service_name: str):
    health = await get_service_health_via_mcp(service_name)
    analysis = build_incident_analysis(health)
    ai_explanation = generate_ai_explanation(health, analysis)

    print(format_report(analysis, ai_explanation))

    print("Structured JSON output:")
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m sre_agent.agent_mcp <service_name>")
        print("Example: python -m sre_agent.agent_mcp checkout")
        sys.exit(1)

    service_name = sys.argv[1]
    asyncio.run(run_agent(service_name))