from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from langgraph_sdk.auth.exceptions import HTTPException
from pydantic import BaseModel

from src.db_history import ensure_session, save_message, get_all_sessions, get_session_history
from src.graph import app
from fastapi.middleware.cors import CORSMiddleware

server = FastAPI(title="Text-to-Action Analyst API")

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace with your frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

class ChatRequest(BaseModel):
    message: str
    thread_id : str

class ApprovalRequest(BaseModel):
    thread_id: str
    approved: bool

@server.post("/chat")
async def chat(request: ChatRequest):
    """
    Run the graph until completion or interruption.
    """

    config = {"configurable" : {"thread_id" : request.thread_id}}
    ensure_session(request.thread_id, title=f"Analysis: {request.message[:20]}...")
    save_message(request.thread_id, "user", request.message)

    inputs = {"messages" : [HumanMessage(content=request.message)]}

    try:
        for _ in app.stream(inputs, config=config):
            pass

        snapshot = app.get_state(config)

        response = {
            "sql_query" : snapshot.values.get("sql_query"),
            "visualization_spec" : snapshot.values.get("visualization_spec"),
            "email_draft" : snapshot.values.get("email_draft"),
            "needs_approval" : snapshot.values.get("needs_approval",False),
            "next_step" : snapshot.next if snapshot.next else None
        }

        ai_content = "I've analyzed the data for you." if response["sql_query"] else "I processed your request."
        save_message(request.thread_id, "assistant", ai_content, response)

        final_response = {
            "status" : "paused" if snapshot.next else "completed",
            **response
        }

        return final_response

    except Exception as ex:
        raise HTTPException(status_code=500,detail=str(ex))

@server.post("/approve")
async def approve(request: ApprovalRequest):
    """
    Resumes the graph execution after human review.
    """
    config = {"configurable" : {"thread_id" : request.thread_id}}

    if not request.approved:
        return {"status" : "cancelled","message" : "Action rejected by user"}

    try:
        for _ in app.stream(None, config=config):
            pass

        return{
            "status" : "completed",
            "message" : "Email sent successfully"
        }

    except Exception as ex:
        raise HTTPException(status_code=500,detail=str(ex))

@server.get("/history")
async def get_history_endpoint():
    """
    Fetched list of all chat sessions.
    """
    try:
        return get_all_sessions()
    except Exception as ex:
        raise HTTPException(status_code=500,detail=str(ex))

@server.get("/history/{thread_id}")
async def get_history_endpoint(thread_id: str):
    """
    Fetches full message history for a specific thread.
    """
    try:
        return get_session_history(thread_id)
    except Exception as ex:
        raise HTTPException(status_code=500,detail=str(ex))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="0.0.0.0", port=8000)