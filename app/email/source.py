from pathlib import Path
import json
import logging
from .schemas import EmailRead
from .invalid_email import InvalidEmailError
from app.config import settings

logger: logging.Logger = logging.getLogger(__name__)


class JSONEmailSource:

    def load(self) -> list[EmailRead]:
        path: Path = self._get_emails_path()
        with open(path, "r", encoding="utf-8") as file:
            emails: list[dict] = json.load(file)
            validated_emails: list[dict] = []
            for email in emails:
                try:
                    self._validate_emails(email)
                    validated_emails.append(email)
                except InvalidEmailError as e:
                    logger.warning(e)

            return list(self._map_emails(validated_emails))

    def _get_emails_path(self) -> Path:
        path: Path = settings.data_dir / "emails.json"
        return path

    def _validate_emails(self, email: dict) -> dict:
        required_keys = ["sender", "subject", "body", "is_read"]
        for key in required_keys:
            if key not in email:
                raise InvalidEmailError(key)

    def _map_emails(self, emails: list[dict]) -> list[EmailRead]:
        mapped_emails: list[EmailRead] = [EmailRead(id=index, **email)
                                          for index, email in enumerate(emails, start=1)]
        return mapped_emails
