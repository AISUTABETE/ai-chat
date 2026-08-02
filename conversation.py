import uuid

from config import SYSTEM_PROMPT, KEEP_MESSAGES
from repository import(
    insert_conversation,
    insert_message,
    select_messages,
    conversation_exists,
    count_messages
)

def create_conversation() -> str:
    conversation_id = str(uuid.uuid4())
    insert_conversation(conversation_id, created_at=None)
    insert_message(conversation_id, "system", SYSTEM_PROMPT, created_at=None)
    return conversation_id

def add_message(conversation_id: str,
                role: str, 
                content: str
    ) -> None:
    if not exists(conversation_id):
        raise ValueError(f"Conversation ID {conversation_id} does not exist.")
    insert_message(conversation_id, role, content, created_at=None)

def get_history(conversation_id: str) -> list[dict[str, str]]:
    return select_messages(conversation_id)

def get_history_length(conversation_id: str) -> int:
    return count_messages(conversation_id)
def exists(conversation_id: str) -> bool:
    return conversation_exists(conversation_id)

def compress_history(conversation_id: str, summary: str) -> None:
    conversation = conversations[conversation_id]
    
    messages = conversation["messages"]
    if len(messages) > KEEP_MESSAGES:
        conversation["messages"] = messages[-KEEP_MESSAGES:]
    
    add_system_message(conversation_id, summary)

def add_system_message(conversation_id: str, summary: str) -> None:
    conversation = conversations[conversation_id]
    system_content = SYSTEM_PROMPT + f"历史对话摘要: {summary}"
    system_message = {
        "role": "system",
        "content": system_content
    }
    conversation["messages"].insert(0, system_message)
