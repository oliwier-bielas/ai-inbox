from fastapi import APIRouter
from .service import analysis_service
from .schema import EmailAnalyseLLM
router = APIRouter(prefix="/email", tags=["analysis"])


@router.post("/{email_id}/analyze")
def analyze_email(email_id: int) -> EmailAnalyseLLM:
    return analysis_service.analyze(email_id)
