from app.core.exceptions import NotFoundError, ServiceUnavailableError


class LLMResponseError(NotFoundError):
    def __init__(self, attempts: int):
        super().__init__(
            f"LLM returned an invalid response after {attempts} attempts")


class LLMUnavailableError(ServiceUnavailableError):
    def __init__(self):
        super().__init__("LLM service is unavailable")
