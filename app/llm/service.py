import logging

import openai
from pydantic import BaseModel, ValidationError

from app.config import settings

from .client import client
from .exceptions import LLMResponseError, LLMUnavailableError

logger: logging.Logger = logging.getLogger(__name__)


class LLMService:
    def analyze[T: BaseModel](
        self, system_prompt: str, user_prompt: str, response_type: type[T]
    ) -> T:
        for attempt in range(1, 3):
            try:
                result = (
                    client.chat.completions.create(
                        model=settings.llm_model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        response_format={
                            "type": "json_schema",
                            "json_schema": {
                                "name": response_type.__name__,
                                "schema": response_type.model_json_schema(),
                            },
                        },
                        temperature=0,
                        max_tokens=500,
                    )
                    .choices[0]
                    .message.content
                )
            except openai.APIConnectionError as e:
                logger.error(f"LLM api connection error: {e}")
                raise LLMUnavailableError()

            try:
                return response_type.model_validate_json(result)
            except ValidationError as e:
                logger.warning(f"LLM returned invalid data: {e}")

        raise LLMResponseError(attempt)


llm_service = LLMService()
