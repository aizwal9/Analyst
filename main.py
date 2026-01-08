from fastapi import FastAPI
from pydantic import BaseModel
# from graph import app_graph

app = FastAPI()


class RequestBody(BaseModel):
    query: str


@app.post("/chat")
async def chat(body: RequestBody):
    # Run the LangGraph workflow
    inputs = {"messages": [{"role": "user", "content": body.query}]}
    result = await app_graph.ainvoke(inputs)

    return {
        "result":result
    }