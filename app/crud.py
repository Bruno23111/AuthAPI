from .firebase import db
from fastapi import HTTPException, status

def create_task(user_id: str, task_data: dict):
    task_data["creator_id"] = user_id
    doc_ref, _ = db.collection("users").document(user_id).collection("tasks").add(task_data)
    # Pega o ID do documento criado
    task_id = doc_ref.id
    # Retorna a task criada, incluindo o id
    return {"task_id": task_id, **task_data}



def list_tasks(user_id: str):
    tasks = db.collection("users").document(user_id).collection("tasks").stream()
    # Incluindo o id do documento junto com os dados
    return [{"task_id": t.id, **t.to_dict()} for t in tasks]

def delete_task(user_id: str, task_id: str):
    task_ref = db.collection("users").document(user_id).collection("tasks").document(task_id)
    task = task_ref.get()
    if not task.exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.to_dict().get("creator_id") != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this task")
    task_ref.delete()
