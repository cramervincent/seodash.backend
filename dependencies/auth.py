from typing import Union, Dict
import time
import jwt
import bcrypt
import os
from schemas.auth import UserLoginSchema
from dependencies.dependencies import *
from dependencies.database import *
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import models

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

SALT = os.getenv('PASSWORD_SALT').encode()


def hashPassword(plain_psw):
    bytes = plain_psw.encode('utf-8')
    return bcrypt.hashpw(bytes, SALT)


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
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def check_user(data: UserLoginSchema, db: Session):
    users = db.query(models.Users).all()
    for user in users:
        print(user.password, '\n', hashPassword(data.password))
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
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
