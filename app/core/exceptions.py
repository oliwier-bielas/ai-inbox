class AppError(Exception):
    status_code: int = 500
    message: str = "Internal error"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.message
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = 404
