from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain_core.prompts import ChatPromptTemplate

from backend.agent.prompt import prompt as system_prompt
from backend.agent.mcp_integration import get_mcp_tools  # async fn
from typing import Any



async def invoke_agent(payload: dict[str, Any]) -> dict[str, Any]:

    tools = await get_mcp_tools()

    agent = create_react_agent(
        prompt=system_prompt,
        model="anthropic:claude-3-7-sonnet-latest",
        tools=tools,
    )

    response = await agent.ainvoke(payload)
    return {"output": response}
