from pydantic import BaseModel, EmailStr
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Task(TaskCreate):
    creator_id: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
