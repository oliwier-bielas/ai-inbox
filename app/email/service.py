from .schemas import EmailRead
from .source import JSONEmailSource
from .exceptions import EmailNotFound


class EmailService:
    def __init__(self, source: JSONEmailSource):
        self._emails: list[EmailRead] = source.load()

    def get_all(self) -> list[EmailRead]:
        return list(self._emails)

    def get_by_id(self, email_id: int) -> EmailRead:
        email: EmailRead | None = next(
            (email for email in self._emails if email.id == email_id), None)

        if email == None:
            raise EmailNotFound

        return email


emails_service = EmailService(JSONEmailSource())
