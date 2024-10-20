from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    email: str

class AuthUser(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

