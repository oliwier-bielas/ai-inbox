from pathlib import Path

from app.email.source import JSONEmailSource


def test_load_skips_invalid_emails(test_emails_path: Path) -> None:
    emails = JSONEmailSource(test_emails_path).load()
    assert len(emails) == 3


def test_load_assigns_ids_without_gaps(test_emails_path: Path) -> None:
    emails = JSONEmailSource(test_emails_path).load()
    assert [email.id for email in emails] == [1, 2, 3]
