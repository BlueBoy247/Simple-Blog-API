import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import models, schemas

def get_user(db: Session, email: str) -> models.User:
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except SQLAlchemyError:
        return None

def create_post(db: Session, post: schemas.BlogPost) -> dict:
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
    try:
        posts = [schemas.BlogPost.model_validate(post) for post in db.query(models.BlogPost).all()]
        return posts
    except SQLAlchemyError:
        return None

def get_post_by_page(db: Session, page: int, pagesize: int) -> list:
    try:
        posts = db.query(models.BlogPost).limit(pagesize).offset((page - 1) * pagesize).all()
        return [schemas.BlogPost.model_validate(post) for post in posts]
    except SQLAlchemyError:
        return None
