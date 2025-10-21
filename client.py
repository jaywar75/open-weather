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
            print("Connected to OpenWeather MCP Server")
            print("Available tools:", [tool.name for tool in tools.tools])

            # Interactive loop
            while True:
                try:
                    city = input("Enter city (or 'quit' to exit): ").strip()
                    if city.lower() == 'quit':
                        break
                    if not city:
                        continue

                    units = input("Units (c/f/k, default c): ").strip() or 'c'
                    lang = input("Language (default en): ").strip() or 'en'

                    # Call the weather tool
                    result = await session.call_tool("weather", {"city": city, "units": units, "lang": lang})
                    print("\nWeather result:")
                    for content in result.content:
                        print(content.text)
                    print("\n" + "="*50 + "\n")
                except Exception as e:
                    print(f"Error: {e}")
                    print("Please try again.\n")

if __name__ == "__main__":
    asyncio.run(main())