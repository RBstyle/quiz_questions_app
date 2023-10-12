from pydantic import BaseModel, Field
from datetime import datetime


class QuestionsNum(BaseModel):
    """Request model. Number of requested questions."""

    questions_num: int = Field(ge=1, description="Number of questions")


class Question(BaseModel):
    """Question model"""

    id: int = Field(description="ID of question")
    question: str = Field(description="Question text")
    answer: str = Field(description="Answer text")
    created_at: datetime = Field(description="Date and time the question was created")
