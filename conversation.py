import uuid

from config import SYSTEM_PROMPT, KEEP_MESSAGES

conversations: dict[str, dict] = {}

def create_conversation() -> str:
    conversation_id = str(uuid.uuid4())
    conversations[conversation_id] = {
        "messages" : [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
    }
    return conversation_id

def add_message(conversation_id: str,
                role: str, 
                content: str
    ) -> None:
    if not exists(conversation_id):
        raise ValueError(f"Conversation ID {conversation_id} does not exist.")
    conversations[conversation_id]["messages"].append(
        {
            "role": role,
            "content": content
        }
    )

def get_history(conversation_id: str) -> list[dict[str, str]]:
    return conversations[conversation_id]["messages"]

def get_history_length(conversation_id: str) -> int:
    return len(conversations[conversation_id]["messages"])

def exists(conversation_id: str) -> bool:
    return conversation_id in conversations

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
