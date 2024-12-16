from fastapi.exceptions import HTTPException
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

from models.response import QAList

load_dotenv()
client = OpenAI()

SYSTEM_MESSAGE = "You are a helpful and knowledgeable assistant specialized in creating educational materials. Your task is to generate question-and-answer pairs to test a student's understanding of a provided source text. The questions should be clear and engaging, designed to assess key concepts and details in the material. Respond in the JSON format provided to you."
MODEL = "gpt-4o-mini"

class Session:
    def __init__(self, id: str, file_pages: List[str], filename: str):
        self.id = id
        self.file_pages = file_pages
        self.filename = filename

    def get_pages(self, start_page: int, end_page: int) -> str:
        if end_page == -1:
            end_page = len(self.file_pages)
        if end_page < start_page:
            raise HTTPException(status_code=400, detail="End page must be greater than or equal to start page.")
        start_page += 1
        return '\n\n'.join(self.file_pages[start_page:end_page])

    def generate_questions(self, start_page: int, end_page: int) -> QAList:
        content = self.get_pages(start_page, end_page)
        completion = client.beta.chat.completions.parse(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": content},
            ],
            response_format=QAList,
        )

        return completion.choices[0].message.parsed
