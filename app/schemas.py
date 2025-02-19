from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

class BlogPost(BaseModel):
    title: str
    content: str
    tags: list

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
