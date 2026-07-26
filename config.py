import os
from dotenv import load_dotenv

load_dotenv()


SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

BASE_URL = "https://api.siliconflow.cn/v1"

MODEL_NAME = "THUDM/GLM-4-9B-0414"

SYSTEM_PROMPT = '''你是一个可爱、友善的 AI 助手。
                回答简洁明了，可以带一点轻松可爱的语气。
                技术问题保持专业准确，不要过度卖萌。'''