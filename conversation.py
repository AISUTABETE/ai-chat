import uuid

from config import SYSTEM_PROMPT

conversations: dict[str, list[dict[str, str]]] = {}

def create_conversation() -> str:
    conversation_id = str(uuid.uuid4())
    conversations[conversation_id] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]
    return conversation_id

def add_message(conversation_id: str,
                role: str, 
                content: str
    ) -> None:
    if not exists(conversation_id):
        raise ValueError(f"Conversation ID {conversation_id} does not exist.")
    conversations[conversation_id].append(
        {
            "role": role,
            "content": content}
    )

def get_history(conversation_id: str) -> list[dict[str, str]]:
    return conversations.get(conversation_id, [])

def exists(conversation_id: str) -> bool:
    return conversation_id in conversations