from pydantic import BaseModel, Field
from typing import Literal


class EmailAnalysisLLM(BaseModel):
    category: Literal["invoice", "meeting", "promotion", "other"]
    priority: Literal["low", "medium", "hight"]
    summary: str = Field(max_length=150)


class EmailAnalysisRead(EmailAnalysisLLM):
    id: int
