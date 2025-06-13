from langgraph.prebuilt import create_react_agent
from agent.nodes.mcp_integration import get_mcp_tools

tools = get_mcp_tools()

agent = create_react_agent(
    "anthropic:claude-3-7-sonnet-latest",
    tools
)

async def invoke_agent(msg: dict):
    
    response = await agent.ainvoke(msg)

    return response