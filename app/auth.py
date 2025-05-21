from fastapi import Request, HTTPException
from firebase_admin import auth

# função de verificação
async def verify_token(request: Request):
    # Verifica se o cabeçalho Authorization está presente
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    # Extrai o token JWT do cabeçalho
    token = auth_header.split("Bearer ")[1]
    # Verifica e decodifica o token
    try:
        # Chama verify_id_token(token) do Firebase Admin SDK
        decoded_token = auth.verify_id_token(token)
        # Retorna os dados do usuário autenticado
        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email")
        }
    # Se o token for inválido (expirado, manipulado, ou não emitido pelo Firebase), lança erro 401
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
