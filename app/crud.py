from .firebase import db
from fastapi import HTTPException, status

def create_task(user_id: str, task_data: dict):
    # Incluir o user_id como creator_id na task_data antes de adicionar
    task_data["creator_id"] = user_id
    return db.collection("users").document(user_id).collection("tasks").add(task_data)

def list_tasks(user_id: str):
    tasks = db.collection("users").document(user_id).collection("tasks").stream()
    return [t.to_dict() for t in tasks]

def delete_task(user_id: str, task_id: str):
    task_ref = db.collection("users").document(user_id).collection("tasks").document(task_id)
    task = task_ref.get()
    if not task.exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.to_dict().get("creator_id") != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this task")
    task_ref.delete()
