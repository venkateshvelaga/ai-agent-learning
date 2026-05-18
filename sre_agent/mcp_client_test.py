import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "sre_agent.mcp_server.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available MCP tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            result = await session.call_tool(
                "get_service_health_tool",
                arguments={"service_name": "checkout"},
            )

            print("\nRaw MCP tool result:")
            print(result)

            print("\nParsed text content:")
            for content in result.content:
                if hasattr(content, "text"):
                    print(content.text)

                    try:
                        print("\nParsed JSON:")
                        print(json.dumps(json.loads(content.text), indent=2))
                    except json.JSONDecodeError:
                        pass


if __name__ == "__main__":
    asyncio.run(main())