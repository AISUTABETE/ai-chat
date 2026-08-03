from datetime import datetime
import uuid

from config import SYSTEM_PROMPT
from repository import(
    delete_old_messages,
    insert_conversation,
    insert_message,
    select_messages,
    conversation_exists,
    count_messages
)

def create_conversation() -> str:
    conversation_id = str(uuid.uuid4())
    insert_conversation(conversation_id, created_at=datetime.now().isoformat())
    insert_message(conversation_id, "system", SYSTEM_PROMPT, created_at=datetime.now().isoformat())
    return conversation_id

def add_message(conversation_id: str, role: str, content: str) -> None:
    if not exists(conversation_id):
        raise ValueError(f"Conversation ID {conversation_id} does not exist.")
    insert_message(conversation_id, role, content, created_at=datetime.now().isoformat())

def get_history(conversation_id: str) -> list[dict[str, str]]:
    return select_messages(conversation_id)

def get_history_length(conversation_id: str) -> int:
    return count_messages(conversation_id)
def exists(conversation_id: str) -> bool:
    return conversation_exists(conversation_id)

def compress_history(conversation_id: str, summary: str) -> None:    
    delete_old_messages(conversation_id)
    add_system_message(conversation_id, summary)

def add_system_message(conversation_id: str, summary: str) -> None:
    system_content = SYSTEM_PROMPT + f"历史对话摘要: {summary}"
    system_message = {
        "role": "system",
        "content": system_content
    }
    add_message(conversation_id, system_message["role"], system_message["content"]) 
