from pydantic import BaseModel, model_validator, PrivateAttr
from typing import List, Optional
from typing_extensions import Self
from fastapi.exceptions import HTTPException
import base64
from io import BytesIO

from utils.pdf import read_pdf

# Check size (5 MB = 5 * 1024 * 1024 bytes)
MAX_SIZE = 5 * 1024 * 1024

class IncomingFile(BaseModel):
    ''' Incoming file type definition '''
    filename: str
    content: str
    content_type: str

    def parse_file_content(self) -> List[str]:
        if self.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Please upload a valid PDF.")
        try:
            content = base64.b64decode(self.content)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error decoding PDF.")
        if len(content) > MAX_SIZE:
            raise HTTPException(status_code=400, detail="Files must not exceed 5MB.")
        try:
            content_bytes = BytesIO(content)
            pdf_content = read_pdf(content_bytes)
            return pdf_content
        except Exception:
            raise HTTPException(status_code=500, detail="Unspecified error in parsing PDF. Please try again later.")    

class SessionRequest(BaseModel):
    file: IncomingFile
    _pages: List[str] = PrivateAttr(default=None)

    @model_validator(mode='after')
    def parse_file(self) -> Self:
        self._pages = self.file.parse_file_content()
        return self

    def get_pages(self) -> List[str]:
        return self._pages
    
    def get_file_name(self) -> str:
        return self.file.filename
    
class QuestionRequest(BaseModel):
    session_id: str
    start_page: Optional[int] = 0
    end_page: Optional[int] = -1