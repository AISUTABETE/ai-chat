from config import MAX_MESSAGES
from conversation import (
    add_message,
    compress_history,
    create_conversation,
    exists,
    get_history,
    get_history_length,
)

from llm import stream_llm, call_llm

async def chat(conversation_id: str, message: str):
    if conversation_id is None or not exists(conversation_id):
        conversation_id = create_conversation()
    
    add_message(conversation_id, "user", message)
    
    if get_history_length(conversation_id) > MAX_MESSAGES:
        await update_summary(conversation_id)
    history = get_history(conversation_id)
    
    response = stream_llm(history)
    answer = ""
    async for chunk in response:
        answer += chunk
        yield chunk
    add_message(conversation_id, "assistant", answer)

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
