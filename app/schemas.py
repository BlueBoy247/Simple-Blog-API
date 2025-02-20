"""
This module contains the Pydantic models for the application.
"""

from pydantic import BaseModel

class User(BaseModel):
    """User model"""

    email: str
    password: str

class BlogPost(BaseModel):
    """Blog post model"""

    title: str
    content: str
    tags: list

    class Config:
        """Config class for BlogPost model"""

        from_attributes = True

class Token(BaseModel):
    """Token model"""

    access_token: str
    token_type: str

class TokenData(BaseModel):
    """TokenData model"""

    email: str | None = None
