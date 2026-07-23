from fastapi import FastAPI
from pydantic import BaseModel
from llm import chat

app = FastAPI()

class ChatRequest(BaseModel):
    conversation_id: str | None = None 
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    answer: str

@app.get("/")
async def root():
    return {
        "message": "Hello, AI Chat!"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    conversation_id, answer = await chat(request.conversation_id, request.message)
    return ChatResponse(conversation_id=conversation_id, answer=answer)


