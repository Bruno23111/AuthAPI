from fastapi import Request, HTTPException, Depends
from firebase_admin import auth

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth_header.split("Bearer ")[-1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
