from typing import Union, Dict
import time
import jwt
import bcrypt
from schemas.auth import UserLoginSchema
from dependencies.dependencies import *
from dependencies.database import *
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models import models

# onderstaande uit env vars halen
JWT_SECRET = "7bc7fbe8d1e74426c42838d44efa62ff4f867ce3a37f96a209586ffcaa79290d"
JWT_ALGORITHM = "HS256"
salt = b'$2b$12$WBW53Ho5naGky3z/P6tmx.' 


# bcrypt.gensalt()
print(salt)

def hashPassword(plain_psw):
    bytes = plain_psw.encode('utf-8')
    return bcrypt.hashpw(bytes, salt)

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 86400
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    print(token)
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def check_user(data: UserLoginSchema, db:Session):
    
    users = db.query(models.Users).all()
    for user in users:
        print(user.email, data.email)
        if user.email == data.email and user.password == hashPassword(data.password):
            return True
    return False 




class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid