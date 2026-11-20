from pydantic import BaseModel


class EmailRead(BaseModel):
    id: int
    sender: str
    subject: str
    body: str
    is_read: bool
