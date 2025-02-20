"""
This module contains the database CRUD operations.
"""

import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import models, schemas

def get_user(db: Session, email: str) -> models.User:
    """
    Get user by email

    Args:
        db (Session): SQLAlchemy session
        email (str): Email of the user

    Returns:
        models.User: User model if found, otherwise None
    """

    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except SQLAlchemyError:
        return None

def create_post(db: Session, post: schemas.BlogPost) -> dict:
    """
    Create a new blog post in the database.

    Args:
        db (Session): SQLAlchemy session for database operations.
        post (schemas.BlogPost): Blog post data including title, content, and tags.

    Returns:
        dict: Result dictionary with a success status. If successful, {"success": True} 
        is returned. If an error occurs, {"success": False, "error": str(e)} is returned 
        with the error message.
    """

    try:
        db_post = models.BlogPost(
            id=int(datetime.datetime.now().timestamp() * 1e6),
            title=post.title,
            content=post.content,
            tags=post.tags
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return {"success": True}
    except SQLAlchemyError as e:
        return {"success": False, "error": str(e)}

def get_all_post(db: Session) -> list:
    """
    Retrieve all blog posts from the database.

    Args:
        db (Session): SQLAlchemy session

    Returns:
        list: List of blog posts, each as a dictionary containing the post title, content, and tags.
    """

    try:
        posts = [schemas.BlogPost.model_validate(post) for post in db.query(models.BlogPost).all()]
        return posts
    except SQLAlchemyError:
        return None

def get_post_by_page(db: Session, page: int, pagesize: int) -> list:
    """
    Retrieve blog posts from the database by page.

    Args:
        db (Session): SQLAlchemy session
        page (int): Page number to retrieve
        pagesize (int): Number of posts to retrieve per page

    Returns:
        list: List of blog posts, each as a dictionary containing the post title, content, and tags.
    """

    try:
        posts = db.query(models.BlogPost).limit(pagesize).offset((page - 1) * pagesize).all()
        return [schemas.BlogPost.model_validate(post) for post in posts]
    except SQLAlchemyError:
        return None
