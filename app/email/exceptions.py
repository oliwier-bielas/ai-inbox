from app.core.exceptions import NotFoundError


class EmailNotFound(NotFoundError):
    def __init__(self, email_id: int) -> None:
        super.__init__(f"Email {email_id} not found")
