import httpx
import openai
import pytest

from app.analysis.schemas import EmailAnalysisLLM
from app.llm.exceptions import LLMResponseError, LLMUnavailableError
from app.llm.service import llm_service

VALID_ANALYSIS = EmailAnalysisLLM(
    category="invoice", priority="high", summary="Pay the invoice"
)


def test_analyze_returns_valid_response(mock_llm_client) -> None:
    calls = mock_llm_client(responses=[VALID_ANALYSIS.model_dump_json()])

    result = llm_service.analyze(
        system_prompt="", user_prompt="", response_type=EmailAnalysisLLM
    )

    assert result == VALID_ANALYSIS
    assert len(calls) == 1


def test_analyze_retries_after_invalid_response(mock_llm_client) -> None:
    calls = mock_llm_client(responses=["not json", VALID_ANALYSIS.model_dump_json()])

    result = llm_service.analyze(
        system_prompt="", user_prompt="", response_type=EmailAnalysisLLM
    )

    assert result == VALID_ANALYSIS
    assert len(calls) == 2


def test_analyze_raises_response_error_after_two_invalid_responses(
    mock_llm_client,
) -> None:
    calls = mock_llm_client(responses=["not json", '{"category": "urgent"}'])

    with pytest.raises(LLMResponseError):
        llm_service.analyze(
            system_prompt="", user_prompt="", response_type=EmailAnalysisLLM
        )

    assert len(calls) == 2


def test_analyze_raises_unavailable_error_without_retry(mock_llm_client) -> None:
    error = openai.APIConnectionError(request=httpx.Request("POST", "http://test"))
    calls = mock_llm_client(error=error)

    with pytest.raises(LLMUnavailableError):
        llm_service.analyze(
            system_prompt="", user_prompt="", response_type=EmailAnalysisLLM
        )

    assert len(calls) == 1
