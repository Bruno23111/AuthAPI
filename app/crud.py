from .firebase import db
from fastapi import HTTPException, status

# função que cria uma nova task para o usuario
# exemplo create_task("user123", {"title": "Estudar Python"})
def create_task(user_id: str, task_data: dict):
    # adiciona o user_id aos dados da task para assim tem um vinculo com quem criou
    task_data["creator_id"] = user_id
    # esse trecho ele esta acessando a coleção users atraves da biblioteca firebase e depois esta 
    # acessando o documento user_id e sucessivamente a subcoleção tasks e adicionando uma task
    doc_ref = db.collection("users").document(user_id).collection("tasks").add(task_data)[1]
    # pega o id do novo documento da tarefa gerado pela FireStore
    task_id = doc_ref.id
    # retorna um dicionario tendo assim como chave o id da task e o valor os dados da mesma
    return {"task_id": task_id, **task_data}

# Retorna todas as tarefas de um usuario
# exemplo list_tasks("user123")
def list_tasks(user_id: str):
    # esse trecho ele esta acessando a coleção users atraves da biblioteca firebase e depois esta
    # acessando o documento user_id e sucessivamente a subcoleção tasks e depois eretorna um gerador com todos os documentos(tasks)
    tasks = db.collection("users").document(user_id).collection("tasks").stream()
    # Incluindo o id do documento junto com os dados em um dicionario
    return [{"task_id": t.id, **t.to_dict()} for t in tasks]

# Deleta uma tarefa veriifiicando se ela existe e se o usuario é o dono dela
# exemplo delete_task("user123", "tarefa2")
def delete_task(user_id: str, task_id: str):
    # acessa o documento dessa task
    task_ref = db.collection("users").document(user_id).collection("tasks").document(task_id)
    # busca os dados dessa task baseado no acesso de cima
    task = task_ref.get()
    # faz uma verificação onde se o documento não existe ele lança o status code de erro 404
    if not task.exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # faz uma verificação se o usuario que esta tentando deletar é realmente o dono da task
    # se ele não for ele retorna o status code de erro 403
    if task.to_dict().get("creator_id") != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this task")
    #deleta a task
    task_ref.delete()