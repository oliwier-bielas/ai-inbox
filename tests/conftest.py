from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.analysis.schemas import EmailAnalysisLLM
from app.email.schemas import EmailRead
from app.email.service import emails_service
from app.email.source import JSONEmailSource
from app.llm.client import client as llm_client
from app.llm.service import llm_service
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


@pytest.fixture
def mock_llm(monkeypatch) -> Callable[..., None]:
    def _mock(
        result: EmailAnalysisLLM | None = None, error: Exception | None = None
    ) -> None:
        def fake_analyze[T: BaseModel](**kwargs) -> T:
            if error:
                raise error

            return result

        monkeypatch.setattr(llm_service, "analyze", fake_analyze)

    return _mock


def fake_response(content: str) -> SimpleNamespace:
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


@pytest.fixture
def mock_llm_client(monkeypatch) -> Callable[..., list]:
    def _mock(
        responses: list[str] | None = None, error: Exception | None = None
    ) -> list:
        calls: list[dict] = []

        def fake_create(**kwargs):
            calls.append(kwargs)
            if error:
                raise error
            return fake_response(responses[len(calls) - 1])

        monkeypatch.setattr(llm_client.chat.completions, "create", fake_create)
        return calls

    return _mock
