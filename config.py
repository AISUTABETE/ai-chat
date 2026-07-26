import os
from dotenv import load_dotenv

load_dotenv()

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

BASE_URL = "https://api.siliconflow.cn/v1"

MODEL_NAME = "THUDM/GLM-4-9B-0414"

MAX_MESSAGES = 8

KEEP_MESSAGES = 4