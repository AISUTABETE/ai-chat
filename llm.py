from openai import AsyncOpenAI
from config import SILICONFLOW_API_KEY, BASE_URL, MODEL_NAME, MAX_MESSAGES
from conversation import *

client = AsyncOpenAI(
    api_key=SILICONFLOW_API_KEY,
    base_url=BASE_URL
)

async def chat(conversation_id: str | None, 
               message: str
    ) -> tuple[str, str]:
    if conversation_id is None or not exists(conversation_id):
        conversation_id = create_conversation()
    
    if get_history_length(conversation_id) > MAX_MESSAGES:
        await update_summary(conversation_id)
    history = get_history(conversation_id)

    add_message(conversation_id, "user", message)
    
    response = await call_llm(history)
    content = response.choices[0].message.content
    
    add_message(conversation_id, "assistant", content)
    
    return conversation_id, content

async def call_llm(messages: list[dict[str, str]]):
    return await client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

async def update_summary(conversation_id: str) -> None:
    history = get_history(conversation_id)
    conversation_text = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in history
        ]
    )
    summary_prompt = f"""
        请总结以下对话，保留关键信息：
        {conversation_text}
        """
    
    response = await call_llm([{"role": "system", "content": summary_prompt}])
    
    summary = response.choices[0].message.content

    compress_history(conversation_id, summary)

