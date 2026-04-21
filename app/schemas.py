from pydantic import BaseModel
from datetime import datetime

class MemoCreate(BaseModel):
    title: str
    content: str

class MemoResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime