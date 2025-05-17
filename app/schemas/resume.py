from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResumeCreate(BaseModel):
    content: str

class ResumeOut(BaseModel):
    id: int
    content: str
    version: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
