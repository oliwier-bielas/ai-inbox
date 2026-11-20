import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("LLM_MODEL"),
    api_key=os.getenv("LLM_API_KEY")
)
