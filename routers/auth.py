from fastapi import APIRouter
from dependencies.dependencies import *
from dependencies.auth import signJWT, hashPassword, check_user
from models import models
from schemas.auth import UserSchema, UserLoginSchema

router = APIRouter()

@router.post("/user/signup")
async def create_user(user: UserSchema, db:Session = Depends(get_db)):
    new_user  = models.Users(
        fullname = user.fullname,
        email = user.email,
        password = hashPassword(user.password)
    )
    db.add(new_user) 
    db.commit()
    return signJWT(user.email)

@router.post("/user/login")
async def user_login(user: UserLoginSchema, db:Session=Depends(get_db)):
    if check_user(user, db):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
        }