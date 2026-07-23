import os
import uuid
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1"
)

conversations: dict[str, list[dict[str, str]]] = {}

async def chat(conversation_id: str | None, message: str) -> tuple[str, str]:
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    conversations[conversation_id].append({"role": "user", "content": message})
    history = conversations[conversation_id]
    response = await client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=history
    )
    content = response.choices[0].message.content
    conversations[conversation_id].append({"role": "assistant", "content": content})
    return conversation_id, content