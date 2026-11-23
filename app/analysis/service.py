from app.email.service import emails_service
from app.llm.service import llm_service
from .prompts import SYSTEM_PROMPT
from .schemas import EmailAnalysisLLM, EmailAnalysisLMMRead


class AnalysisService:

    def analyze(self, email_id: int) -> EmailAnalysisLMMRead:
        email = emails_service.get_by_id(email_id)
        user_prompt = f"Subject: {email.subject}\n\nBody:\n{email.body}"
        analyzed_email = llm_service.analyze(
            system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt, response_type=EmailAnalysisLLM)

        return EmailAnalysisLMMRead(
            id=email.id,
            **analyzed_email.model_dump()
        )


analysis_service = AnalysisService()
