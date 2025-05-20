
## Como Rodar e Testar a API via Postman

### 1. Pré-requisitos

* Python 3.10+ instalado
* Firebase configurado com o arquivo `firebase-credentials.json` na raiz do projeto
* API rodando localmente (exemplo: `http://127.0.0.1:8000`)
* Postman instalado

---

### 2. Executando a API

No terminal, rode:

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:
`http://127.0.0.1:8000`

---

### 3. Obter Token de Autenticação (idToken)

Antes de chamar qualquer endpoint protegido, você precisa gerar o token JWT do Firebase para autenticação.

Faça uma requisição POST para o endpoint do Firebase Authentication para login:

```
POST https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=SEU_API_KEY
Content-Type: application/json
```

Body (JSON):

```json
{
  "email": "usuario@exemplo.com",
  "password": "senha_do_usuario",
  "returnSecureToken": true
}
```

Resposta esperada (exemplo):

```json
{
  "idToken": "SEU_TOKEN_JWT_AQUI",
  "refreshToken": "TOKEN_REFRESH",
  "expiresIn": "3600",
  "localId": "uid_do_usuario",
  ...
}
```

**Guarde o valor do `idToken`, ele será usado no header das requisições.**

---

### 4. Usar Token para acessar a API

Em todas as requisições para endpoints protegidos, adicione no cabeçalho HTTP:

```
Authorization: Bearer SEU_ID_TOKEN_AQUI
```

---

### 5. Endpoints da API no Postman

#### Criar Usuário

* **Método:** POST
* **URL:** `http://127.0.0.1:8000/api/users`
* **Headers:**

  * `Authorization: Bearer SEU_ID_TOKEN_AQUI`
  * `Content-Type: application/json`
* **Body:**

```json
{
  "email": "novo_usuario@exemplo.com",
  "password": "senha_segura"
}
```

---

#### Listar Usuários

* **Método:** GET
* **URL:** `http://127.0.0.1:8000/api/users`
* **Headers:**

  * `Authorization: Bearer SEU_ID_TOKEN_AQUI`

Resposta:

```json
[
  {
    "uid": "uid1",
    "email": "usuario1@exemplo.com",
    "display_name": null,
    "disabled": false
  },
  {
    "uid": "uid2",
    "email": "usuario2@exemplo.com",
    "display_name": "Nome do Usuário",
    "disabled": false
  }
]
```

---

#### Deletar Usuário

* **Método:** DELETE
* **URL:** `http://127.0.0.1:8000/api/users/{uid}`
* **Headers:**

  * `Authorization: Bearer SEU_ID_TOKEN_AQUI`

Resposta:

```json
{
  "message": "Usuário deletado com sucesso"
}
```
#### Criar Task

*   **Método:** POST
*   **URL:** `http://127.0.0.1:8000/tasks`
*   **Headers:**
    *   `Authorization: Bearer SEU_ID_TOKEN_AQUI`
    *   `Content-Type: application/json`
*   **Body:**
json { "title": "Título da Task", "description": "Descrição opcional da task", "completed": false }
---

#### Deletar Task

*   **Método:** DELETE
*   **URL:** `http://127.0.0.1:8000/tasks/{task_id}`
*   **Headers:**
    *   `Authorization: Bearer SEU_ID_TOKEN_AQUI`

    Substitua `{task_id}` pelo ID da task que você deseja deletar. Apenas o criador da task pode apagá-la.

---

### 6. Observações

* O token expira em 1 hora; refaça o login para obter um novo token quando necessário.
* Para mais informações, consulte a [documentação oficial do Firebase Authentication](https://firebase.google.com/docs/auth/rest).

---
