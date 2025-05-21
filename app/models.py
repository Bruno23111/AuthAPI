from pydantic import BaseModel, EmailStr
from typing import Optional

# modelo definido para criar uma task 
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# modelo usado para representar uma tarefa completa
# nesse modelo especifico a classe Task esta herdando tudo da TaskCreate e esta adicionando o campo creator_id
class Task(TaskCreate):
    creator_id: str

# modelo usado para criar um novo usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: str
