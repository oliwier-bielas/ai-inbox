from app.email.service import emails_service
from app.llm.service import llm_service
from .prompts import SYSTEM_PROMPT
from .schema import EmailAnalyseLLM


class AnalysisService:
    def __init__(self):
        pass

    def analyze(self, email_id: int) -> EmailAnalyseLLM:
        email = emails_service.get_by_id(email_id)
        user_prompt = f"Subject: {email.subject}\n\nBody:\n{email.body}"
        analyzed_email = llm_service.analyze(
            system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt, response_type=EmailAnalyseLLM)
        return analyzed_email


analysis_service = AnalysisService()
