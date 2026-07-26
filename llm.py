from openai import AsyncOpenAI
from config import SILICONFLOW_API_KEY, BASE_URL, MODEL_NAME
from conversation import create_conversation, add_message, get_history, exists

client = AsyncOpenAI(
    api_key=SILICONFLOW_API_KEY,
    base_url=BASE_URL
)

async def chat(conversation_id: str | None, 
               message: str
    ) -> tuple[str, str]:
    if conversation_id is None or not exists(conversation_id):
        conversation_id = create_conversation()
        
    add_message(conversation_id, "user", message)
    
    history = get_history(conversation_id)
    
    response = await call_llm(history)
    content = response.choices[0].message.content
    
    add_message(conversation_id, "assistant", content)
    
    return conversation_id, content

async def call_llm(history):
    return await client.chat.completions.create(
        model=MODEL_NAME,
        messages=history
    )