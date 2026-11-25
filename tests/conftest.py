from collections.abc import Callable
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.analysis.schemas import EmailAnalysisLLM
from app.email.schemas import EmailRead
from app.email.service import emails_service
from app.email.source import JSONEmailSource
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
        def fake_analyze[T: BaseModel](
            system_prompt: str, user_prompt: str, response_type: type[T]
        ) -> T:
            if error:
                raise error

            return result

        monkeypatch.setattr(llm_service, "analyze", fake_analyze)

    return _mock
