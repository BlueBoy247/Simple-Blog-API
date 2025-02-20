"""
This module contains the database models.
"""

from sqlalchemy import Column, String, Text, JSON
from app.database import Base

class User(Base):
    """User model"""

    __tablename__ = "users"
    email = Column("email", String(255), primary_key = True, nullable = False)
    password = Column("pwd", String(60), nullable = False)

class BlogPost(Base):
    """Blog post model"""

    __tablename__ = "posts"
    id = Column("id", String(16), primary_key = True, nullable = False)
    title = Column("title", Text, nullable = False)
    content = Column("content", Text)
    tags = Column("tags", JSON)
