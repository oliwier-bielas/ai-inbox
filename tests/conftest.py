from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.email.schemas import EmailRead
from app.email.service import emails_service
from app.email.source import JSONEmailSource
from app.main import app

TEST_DATA_PATH: Path = Path(__file__).parent / "data" / "emails.json"


@pytest.fixture(autouse=True)
def use_test_emails(monkeypatch) -> None:
    test_emails: list[EmailRead] = JSONEmailSource(TEST_DATA_PATH).load()
    monkeypatch.setattr(emails_service, "_emails", test_emails)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_emails_path() -> Path:
    return TEST_DATA_PATH
