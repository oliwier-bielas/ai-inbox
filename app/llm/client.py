from openai import OpenAI

from app.config import settings

client = OpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
    timeout=120,
    max_retries=0,
)
