import asyncio
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

async def main():
    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        print("Please set OWM_API_KEY in .env file")
        return

    # Run the MCP server in Docker
    server_params = StdioServerParameters(
        command="docker",
        args=["run", "--rm", "-i", "-e", f"OWM_API_KEY={api_key}", "mcp-weather"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools])

            # Call the weather tool
            result = await session.call_tool("weather", {"city": "London", "units": "c", "lang": "en"})
            print("Weather result:")
            for content in result.content:
                print(content.text)

if __name__ == "__main__":
    asyncio.run(main())