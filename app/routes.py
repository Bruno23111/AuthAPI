from fastapi import APIRouter, HTTPException, status, Depends
from firebase_admin import auth
from .auth import verify_token
from .models import TaskCreate, UserCreate
from .crud import create_task, list_tasks, delete_task
from fastapi.responses import JSONResponse
from fastapi import status, Depends
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# End point utilizando o metodo HTTP Post que é usado para criar uma nova task
@router.post("/tasks", status_code=status.HTTP_201_CREATED)
# essa função vai receber o objeto task baseado no modelo TaskCreate e varificação de token do usuario
def add_task(task: TaskCreate, user_data=Depends(verify_token)):
    # converte o objeto task em um dicionário
    task_data = task.dict()
    # adiciona  o creator_id com o uid do usuario autenticado
    task_data["creator_id"] = user_data["uid"]
    # chamada da função create_task para salvar a tark no FIrebase
    created_task = create_task(user_data["uid"], task_data)

    # esse é o json de response com uma mensagem de sucesso
    response_data = {
        "task": created_task,
        "message": "Task criada com sucesso"
    }

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(response_data)
    )

# End point utilizando o metodo HTTP GET que é usado para listar as tasks
@router.get("/tasks")
 #essa função requer a autenticação na passagem de parametros
def get_tasks(user_data=Depends(verify_token)):
    # retorna a lista de tasks do usuario (uid) usando list_tasks
    return list_tasks(user_data["uid"])

# End point utilizando o metodo HTTP POST que é Criar Usuarios
@router.post("/users", status_code=status.HTTP_201_CREATED)
# recebe os dados do novo usuario email e password e verifica se o mesmo esta autenticado
def create_user(user: UserCreate, user_data=Depends(verify_token)):
    # cria o novo usuario no FireBase Authentication e retorna o uid e email
    try:
        new_user = auth.create_user(
            email=user.email,
            password=user.password,
        )
        return {"uid": new_user.uid, "email": new_user.email}
    # tratamento de erros como a tentativa de cadastramento de um email ja cadastrado
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# End point utilizando o metodo HTTP GET para Listar os Usuários
@router.get("/users")
#lista todos os usuarios registrado no Firebase Autjentication
def list_users(user_data=Depends(verify_token)):
    # Faz uma iteração nos usuarios coletando uid, email,display_name e se esta diseable
    try:
        users = []
        page = auth.list_users().iterate_all()
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

# End point utilizando o metodo HTTP DELETE para excluir usuarios
@router.delete("/users/{uid}", status_code=status.HTTP_204_NO_CONTENT)
# deleta usuarios por uid informado
def delete_user(uid: str, user_data=Depends(verify_token)):
    try:
        auth.delete_user(uid)
        return {"message": "Usuário deletado com sucesso"}
    # excessões caso o usuario não existir retorna o status code 404
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # excessões para demais casos retorna o status code 500
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# End point utilizando o metodo HTTP DELETE para excluir tarefas
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
# faz a deleção da task apenas se o usuario for o criador
def remove_task(task_id: str, user_data=Depends(verify_token)):
    delete_task(user_data["uid"], task_id)
    return {"message": "Task deleted successfully"}
