from fastapi import APIRouter, HTTPException, status, Depends
from firebase_admin import auth
from .auth import verify_token
from .models import Task, UserCreate
from .crud import create_task, list_tasks

router = APIRouter()

@router.post("/tasks")
def add_task(task: Task, user_data=Depends(verify_token)):
    create_task(user_data["uid"], task.dict())
    return {"message": "Task created"}

@router.get("/tasks")
def get_tasks(user_data=Depends(verify_token)):
    return list_tasks(user_data["uid"])

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, user_data=Depends(verify_token)):
    try:
        new_user = auth.create_user(
            email=user.email,
            password=user.password,
        )
        return {"uid": new_user.uid, "email": new_user.email}
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
