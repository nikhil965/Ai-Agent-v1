"""
server.py — thin FastAPI wrapper around the existing Agent (agent.py)
Drop this file in the SAME folder as agent.py, config.py, tools.py etc.

Run:
    pip install fastapi uvicorn
    uvicorn server:app --reload --port 8000

Then open http://127.0.0.1:8000 in the browser.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agent import Agent  # your existing Agent class, unchanged

app = FastAPI(title="AI Agent API")

# Allow the frontend (served from the same app, but keeping this open
# makes local dev easier if you ever split frontend/backend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# One shared Agent instance. If your Agent keeps conversation memory
# internally (via memory.py), this means all requests share one session —
# fine for a single-user local tool like this.
agent = Agent()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


# NOTE: endpoint changed from /api/chat to /chat to match the
# API_ENDPOINT used by static/index.html (const API_ENDPOINT = "/chat";)
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        reply = agent.run(req.message)
        return ChatResponse(response=reply)
    except Exception as e:
        return ChatResponse(response=f"Error: {e}")


# Serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")