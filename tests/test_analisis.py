from fastapi.testclient import TestClient

from app.analysis.schemas import EmailAnalysisLLM
from app.llm.exceptions import LLMUnavailableError


def test_analyze_email(client: TestClient, mock_llm) -> None:
    MOCK_ANALYSIS = {
        "category": "invoice",
        "priority": "high",
        "summary": "Pay the invoice",
    }
    llm_mock_response = EmailAnalysisLLM(**MOCK_ANALYSIS)
    mock_llm(llm_mock_response)

    email_id = 1
    res = client.post(f"/emails/{email_id}/analyze")

    assert res.json() == {"id": email_id, **MOCK_ANALYSIS}


def test_analyze_email_when_llm_is_down(client: TestClient, mock_llm) -> None:
    error = LLMUnavailableError()
    mock_llm(error=error)

    email_id = 1
    res = client.post(f"/emails/{email_id}/analyze")

    assert res.json() == {"detail": error}
