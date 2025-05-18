from fastapi import APIRouter, HTTPException, status, Depends
from firebase_admin import auth
from .auth import verify_token
from .models import Task, UserCreate
from .crud import create_task, list_tasks, delete_task

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

@router.get("/users")
def list_users(user_data=Depends(verify_token)):
    try:
        users = []
        page = auth.list_users().iterate_all()  # lista todos os usuários
        for user in page:
            users.append({
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "disabled": user.disabled,
            })
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/users/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(uid: str, user_data=Depends(verify_token)):
    try:
        auth.delete_user(uid)
        return {"message": "Usuário deletado com sucesso"}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: str, user_data=Depends(verify_token)):
    delete_task(user_data["uid"], task_id)
    return {"message": "Task deleted successfully"}
