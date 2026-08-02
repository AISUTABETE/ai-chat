from openai import AsyncOpenAI
from config import SILICONFLOW_API_KEY, BASE_URL, MODEL_NAME

client = AsyncOpenAI(
    api_key=SILICONFLOW_API_KEY,
    base_url=BASE_URL
)

async def call_llm(messages: list[dict[str, str]]):
    return await client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

async def stream_llm(messages: list[dict[str, str]]):
    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=True
    )
    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content

