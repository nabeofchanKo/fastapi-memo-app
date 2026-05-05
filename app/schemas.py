from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MemoCreate(BaseModel):
    title: str
    content: str

class MemoResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)