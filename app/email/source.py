import json
import logging
from pathlib import Path

from pydantic import ValidationError

from app.config import settings

from .schemas import EmailRead

logger: logging.Logger = logging.getLogger(__name__)


class JSONEmailSource:
    def load(self) -> list[EmailRead]:
        path: Path = self._get_emails_path()
        with open(path, "r", encoding="utf-8") as file:
            emails: list[dict] = json.load(file)
            mapped_emails: list[EmailRead] = []
            mail_id = 1
            for email in emails:
                try:
                    mapped_emails.append(EmailRead(id=mail_id, **email))
                    mail_id += 1
                except ValidationError as e:
                    logger.warning(f"Warning: skipping invalid email: {e}")

            return list(mapped_emails)

    def _get_emails_path(self) -> Path:
        path: Path = settings.data_dir / "emails.json"
        return path
