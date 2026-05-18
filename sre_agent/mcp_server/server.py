from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from sre_agent.tools.monitoring_tools import get_service_health


load_dotenv()

mcp = FastMCP("sre-monitoring-mcp-server")


@mcp.tool()
def get_service_health_tool(service_name: str) -> dict:
    """
    Get synthetic health data for a service from the mock monitoring API.

    Args:
        service_name: Name of the service to check, such as checkout, payment, or order.

    Returns:
        Service health data including status, availability, latency, error rate, recent change, and timestamp.
    """
    return get_service_health(service_name)


if __name__ == "__main__":
    mcp.run()