from app.core.exceptions import NotFoundError


class LLMResponseError(NotFoundError):
    def __init__(self, attempts: int):
        super().__init__(
            f"LLM returned an invalid response after {attempts} attempts")
