from pydantic import BaseModel
from datetime import datetime


class QuestionsNum(BaseModel):
    questions_num: int


class Question(BaseModel):
    id: int
    original_id: int
    question: str
    answer: str
    created_at: datetime
