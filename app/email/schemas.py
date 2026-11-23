from pydantic import BaseModel, field_validator


class EmailRead(BaseModel):
    id: int
    sender: str
    subject: str
    body: str
    is_read: bool

    @field_validator("sender", "subject", "body")
    @classmethod
    def field_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value.strip()
