from pydantic import BaseModel

class Blogpost(BaseModel):
    title: str
    content: str
    tags: str | list

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
