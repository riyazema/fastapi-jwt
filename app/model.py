from pydantic import BaseModel, EmailStr


class PostSchema(BaseModel):
    id: int 
    title: str 
    content: str 


class UserSchema(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

