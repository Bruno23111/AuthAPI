from .firebase import db

def create_task(user_id: str, task_data: dict):
    return db.collection("users").document(user_id).collection("tasks").add(task_data)

def list_tasks(user_id: str):
    tasks = db.collection("users").document(user_id).collection("tasks").stream()
    return [t.to_dict() for t in tasks]
