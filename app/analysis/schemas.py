from typing import Literal

from pydantic import BaseModel, Field


class EmailAnalysisLLM(BaseModel):
    category: Literal["invoice", "meeting", "promotion", "other"]
    priority: Literal["low", "medium", "high"]
    summary: str = Field(max_length=150)


class EmailAnalysisRead(EmailAnalysisLLM):
    id: int
