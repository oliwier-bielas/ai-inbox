from pydantic import BaseModel
from .client import client
from app.config import settings


class LLMService():
    def analyze[T: BaseModel](self, system_prompt: str, user_prompt: str, response_type: type[T]) -> T:
        message = [{"role": "SYSTEM", "message": user_prompt}]
        print(message)
        result = client.responses.create(
            model=settings.llm_model,
            instructions=system_prompt,
            input=user_prompt
        )
        return response_type.model_validate_json(result.output_text)


llm_service = LLMService()
