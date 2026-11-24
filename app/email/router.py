from fastapi import APIRouter

from .schemas import EmailRead
from .service import emails_service

router = APIRouter(prefix="/emails", tags=["emails"])


@router.get("")
def get_all_emails() -> list[EmailRead]:
    return emails_service.get_all()


@router.get("/{email_id}")
def get_email_by_id(email_id: int) -> EmailRead:
    return emails_service.get_by_id(email_id)
