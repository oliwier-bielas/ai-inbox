from collections.abc import Callable

from fastapi.testclient import TestClient

from app.analysis.schemas import EmailAnalysisLLM
from app.email.exceptions import EmailNotFoundError
from app.llm.exceptions import LLMResponseError, LLMUnavailableError


def test_analyze_email(client: TestClient, mock_llm: Callable[..., None]) -> None:
    MOCK_ANALYSIS = {
        "category": "invoice",
        "priority": "high",
        "summary": "Pay the invoice",
    }
    llm_mock_response = EmailAnalysisLLM(**MOCK_ANALYSIS)
    mock_llm(llm_mock_response)

    email_id = 1
    res = client.post(f"/emails/{email_id}/analyze")

    assert res.status_code == 200
    assert res.json() == {"id": email_id, **MOCK_ANALYSIS}


def test_anylyze_email_by_fake_id(client: TestClient) -> None:
    email_id = 99
    res = client.post(f"/emails/{email_id}/analyze")
    assert res.status_code == 404
    assert res.json() == {"detail": EmailNotFoundError(email_id).message}


def test_analyze_email_when_llm_is_down(
    client: TestClient, mock_llm: Callable[..., None]
) -> None:
    error = LLMUnavailableError()
    mock_llm(error=error)

    email_id = 1
    res = client.post(f"/emails/{email_id}/analyze")

    assert res.status_code == 503
    assert res.json() == {"detail": error.message}


def test_analyze_email_when_llm_returns_incorrect_data(
    client: TestClient, mock_llm: Callable[..., None]
) -> None:
    error = LLMResponseError(attempts=3)
    mock_llm(error=error)

    email_id = 1
    res = client.post(f"/emails/{email_id}/analyze")

    assert res.status_code == 502
    assert res.json() == {"detail": error.message}
