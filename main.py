from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from chat import chat
from conversation import create_conversation
from database import init_database

init_database()

app = FastAPI()

class ChatRequest(BaseModel):
    conversation_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str


@app.get("/")
async def root():
    return {"message": "Hello, AI Chat!"}


@app.post("/chat")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        chat(request.conversation_id, request.message),
        media_type="text/plain"
    )


@app.post("/conversation")
def create_conversation_endpoint():
    conversation_id = create_conversation()
    return {"conversation_id": conversation_id}
