from pydantic import BaseModel
from datetime import date


# Define a response model using Pydantic
class AnswerResponse(BaseModel):
    question: str
    answer: dict
    date: date