from langchain_mcp_adapters.client import MultiServerMCPClient


client = MultiServerMCPClient({
    "google_workspace": {
        "command": "python",
        "args": ["./backend/google_workspace_mcp/main.py", "--transport", "stdio"],
        "env": {
            "WORKSPACE_MCP_PORT": "9000",
            "WORKSPACE_MCP_BASE_URI": "http://localhost"
        },
        "transport": "stdio",
    }
})


tools_cache = None  # cache once loaded

async def get_mcp_tools():
    global tools_cache
    if tools_cache is None:
        tools_cache = await client.get_tools()
    return tools_cache