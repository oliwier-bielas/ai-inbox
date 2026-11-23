from fastapi import APIRouter
from .service import analysis_service
from .schemas import EmailAnalysisRead
router = APIRouter(prefix="/emails", tags=["analysis"])


@router.post("/{email_id}/analyze")
def analyze_email(email_id: int) -> EmailAnalysisRead:
    return analysis_service.analyze(email_id)
