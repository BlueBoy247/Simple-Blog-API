"""
This module contains the blog router, which handles operations related to blog posts,
such as retrieving all posts, retrieving posts by page, and creating new posts.
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.routers.login import get_current_user

router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
)

@router.get("/all")
async def get_all_post(db: Session = Depends(get_db)) -> list:
    """
    Retrieve all blog posts from the database.

    Args:
        db (Session): SQLAlchemy session

    Returns:
        list: List of blog posts, each as a dictionary containing the post title, content, and tags.
    """

    return crud.get_all_post(db)

@router.get("/page/{page}")
async def get_post_by_page(page: int, pagesize: int = 10, db: Session = Depends(get_db)) -> list:
    """
    Retrieve blog posts from the database by page.

    Args:
        page (int): Page number to retrieve
        pagesize (int): Number of posts to retrieve per page (default: 10)
        db (Session): SQLAlchemy session

    Returns:
        list: List of blog posts, each as a dictionary containing the post title, content, and tags.
    """

    return crud.get_post_by_page(db, page, pagesize)

@router.post("/create", dependencies=[Depends(get_current_user)])
async def create_post(blog_post: schemas.BlogPost, db: Session = Depends(get_db)) -> dict:
    """
    Create a new blog post in the database.

    Args:
        blog_post (schemas.BlogPost): Blog post data including title, content, and tags.
        db (Session): SQLAlchemy session

    Returns:
        dict: Result dictionary with a success status. If successful, {"message": "success"} 
        is returned. If an error occurs, {"success": False, "error": str(e)} is returned 
        with the error message.
    """

    result = crud.create_post(db, blog_post)
    if result["success"]:
        return {"message": "success"}
    raise HTTPException(status_code=500, detail=result["error"])
