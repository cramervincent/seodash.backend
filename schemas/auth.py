from pydantic import BaseModel

class UserSchema(BaseModel):
    fullname: str
    email: str
    password: str
    role:str



class UserLoginSchema(BaseModel):
    email: str
    password: str

