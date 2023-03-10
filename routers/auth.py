from fastapi import APIRouter
from dependencies.dependencies import *
from dependencies.auth import signJWT, hashPassword, check_user, JWTBearer
from models import models
from schemas.auth import UserSchema, UserLoginSchema

router = APIRouter()


@router.get("/users", dependencies=[Depends(JWTBearer())])
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.post("/user/signup", dependencies=[Depends(JWTBearer())])
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_user = models.Users(
        fullname=user.fullname,
        email=user.email,
        password=hashPassword(user.password)
    )
    db.add(new_user)
    db.commit()
    return signJWT(user.email)


@router.post("/user/login")
async def user_login(user: UserLoginSchema, db: Session = Depends(get_db)):
    nm_of_users = db.query(models.Users).all()
    
    if len(nm_of_users) == 0:
        
        new_user = models.Users(
            fullname='Admin',
            email=user.email,
            role='admin',
            password=hashPassword(user.password)
        )
        db.add(new_user)
        db.commit()
        return signJWT(user.email)

    if not check_user(user, db):
        raise HTTPException(
            status_code=401, detail='Gebruikersnaam en/of wachtwoord niet correct.')

    return signJWT(user.email)

@router.delete("/users", dependencies=[Depends(JWTBearer())])
async def delete_all_users(db: Session = Depends(get_db)):
    allusers = db.query(models.Users).all()
    for user in allusers:
        db.delete(user)
    db.commit()
    return "Alle users verwijderd."