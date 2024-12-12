from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from uuid import uuid4

from session import Session
from models.api_input import SessionRequest, QuestionRequest
from models.response import QAList
from utils.session_end import schedule_session_end

app = FastAPI()

sessions: Dict[str, Session] = {}

@app.put("/session")
async def new_session(request: SessionRequest) -> str:
    file_content = request.get_pages()
    session_id = uuid4()
    session = Session(session_id, file_content)
    sessions[session_id] = session

    # Clear session from the container after 4 hours
    schedule_session_end(session_id, 14400)

    return session_id

@app.post("/questions", response_model=QAList)
def generate_questions(request: QuestionRequest):
    session = sessions.get(request.session_id)
    if not session:
        raise HTTPException("Session not found.")
    return session.generate_questions(request.start_page, request.end_page)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if end_page == -1:
#     end_page = 99999
# if end_page < start_page:
#     raise HTTPException(status_code=400, detail="End page must be greater than or equal to start page.")

    