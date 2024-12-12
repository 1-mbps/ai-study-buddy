from fastapi.exceptions import HTTPException
from typing import List

from models.response import QAList

class Session:
    def __init__(self, id: str, file_pages: List[str]):
        self.id = id
        self.file_pages = file_pages

    def generate_questions(self, start_page: int, end_page: int) -> QAList:
        if end_page == -1:
            end_page = len(self.file_pages)
        if end_page < start_page:
            raise HTTPException(status_code=400, detail="End page must be greater than or equal to start page.")
        start_page += 1
        return '\n\n'.join(self.file_pages[start_page:end_page])