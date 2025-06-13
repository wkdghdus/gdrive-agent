from langchain_mcp_adapters.client import MultiServerMCPClient


client = MultiServerMCPClient(
    {
        "google_workspace_mcp": {
            # port 8000 is the default port. If you wish to change the port use command `export WORKSPACE_MCP_PORT="9000"`
            # make sure to change auth in client_secret.json.
            # https://workspacemcp.com/quick-start refer to this link for more info
            "url": "http://localhost:8000/oauth2callback",
            "transport": "streamable_http",
        }
    }
)

async def get_mcp_tools():

    tools = await client.get_tools()

    return tools