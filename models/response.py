from pydantic import BaseModel
from typing import List

class SessionResponse(BaseModel):
    session_id: str
    session_name: str

class QA(BaseModel):
    question: str
    answer: str

class QAList(BaseModel):
    qa_list: List[QA]