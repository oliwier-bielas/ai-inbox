from pydantic import BaseModel
from .client import client
from app.config import settings
from pydantic import ValidationError
import logging
from .exceptions import LLMResponseError

logger: logging.Logger = logging.getLogger(__name__)


class LLMService():
    def analyze[T: BaseModel](self, system_prompt: str, user_prompt: str, response_type: type[T]) -> T:
        for attempts in range(1, 3):
            result = client.responses.create(
                model=settings.llm_model,
                instructions=system_prompt,
                input=user_prompt
            )

            try:
                return response_type.model_validate_json(result.output_text)
            except ValidationError as e:
                logger.warning(f"LLM returned invalid data: {e}")

        raise LLMResponseError(attempts)


llm_service = LLMService()
