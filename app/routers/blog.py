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
    return crud.get_all_post(db)

@router.get("/page/{page}")
async def get_post_by_page(page: int, pagesize: int = 10, db: Session = Depends(get_db)) -> list:
    return crud.get_post_by_page(db, page, pagesize)

@router.post("/create", dependencies=[Depends(get_current_user)])
async def create_post(blog_post: schemas.BlogPost, db: Session = Depends(get_db)) -> dict:
    result = crud.create_post(db, blog_post)
    print(result)
    if result["success"]:
        return {"message": "success"}
    raise HTTPException(status_code=500, detail=result["error"])
