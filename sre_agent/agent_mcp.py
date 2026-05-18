import sys
import os
import json
import asyncio

from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from sre_agent.ai.gemini_explainer import generate_ai_explanation
from sre_agent.reporting.report_formatter import format_report

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


async def run_agent(service_name: str):
    health = await get_service_health_via_mcp(service_name)
    analysis = build_incident_analysis(health)
    ai_explanation = generate_ai_explanation(health, analysis)

    print(format_report(analysis, ai_explanation, execution_mode="MCP-based agent"))

    print("Structured JSON output:")
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m sre_agent.agent_mcp <service_name>")
        print("Example: python -m sre_agent.agent_mcp checkout")
        sys.exit(1)

    service_name = sys.argv[1]
    asyncio.run(run_agent(service_name))