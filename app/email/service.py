from .schemas import EmailRead
from .source import JSONEmailSource


class EmailService:
    def __init__(self, source: JSONEmailSource):
        self._emails = source.load()


emails_service = EmailService(JSONEmailSource())
