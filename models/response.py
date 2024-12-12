from pydantic import BaseModel
from typing import List

class QA(BaseModel):
    question: str
    answer: str

class QAList(BaseModel):
    qa_list: List[QA]