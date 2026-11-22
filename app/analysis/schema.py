from pydantic import BaseModel


class EmailAnalyseLLM(BaseModel):
    category: str
    priority: str
    summary: str
