import os
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.agent.agent import invoke_agent
from backend.agent.mcp_integration import get_mcp_tools

load_dotenv()

app = FastAPI()

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ————————————————
# 1) Startup event to keep MCP alive
# ————————————————

@app.on_event("startup")
async def warmup_mcp():
    try:
        await get_mcp_tools()  # Boot the MCP subprocess once
        print("✅ MCP subprocess initialized and ready.")
    except Exception as e:
        print("❌ Failed to initialize MCP tools:", e)

# ————————————————
# 2) Auth status for frontend
# ————————————————

@app.get("/auth/status")
async def auth_status():
    return {"connected": True}

# ————————————————
# 3) Chat endpoint
# ————————————————

class ChatRequest(BaseModel):
    message: str
    contextIds: list[str] = []

class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    payload = {
        "messages": [
            {"role": "user", "content": req.message}
        ]
    }

    result = await invoke_agent(payload)
    return ChatResponse(reply=result["output"]["messages"][-1].content)

# ————————————————
# 4) Static frontend
# ————————————————

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
app.mount(
    "/",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="static",
)
