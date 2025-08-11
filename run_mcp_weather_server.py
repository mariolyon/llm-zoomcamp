import asyncio
from fastmcp import Client
import json

async def main():
    async with Client("weather_server.py") as mcp_client:
        mcp_client.start_server()
        mcp_client.initialize()
        mcp_client.initialized()
        mcp_client.get_tools()
        mcp_client.call_tool('get_weather', {'city': 'Berlin'})



class MCPTools:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
        self.tools = None

    def get_tools(self):
        if self.tools is None:
            mcp_tools = self.mcp_client.get_tools()
            self.tools = convert_tools_list(mcp_tools)
        return self.tools

    def function_call(self, tool_call_response):
        function_name = tool_call_response.name
        arguments = json.loads(tool_call_response.arguments)

        result = self.mcp_client.call_tool(function_name, arguments)

        return {
            "type": "function_call_output",
            "call_id": tool_call_response.call_id,
            "output": json.dumps(result, indent=2),
        }

if __name__ == "__main__":
    test = asyncio.run(main())
