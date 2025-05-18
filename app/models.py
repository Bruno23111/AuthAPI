from pydantic import BaseModel, EmailStr
from typing import Optional

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    creator_id: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
