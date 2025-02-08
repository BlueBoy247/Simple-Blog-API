from fastapi import Depends, APIRouter
from app.database import fake_db as db
from app.schemas import Blogpost
from app.routers.login import get_current_user

router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
)

@router.get("/all")
async def get_all() -> dict:
    return db["blogs"]

@router.post("/create", dependencies=[Depends(get_current_user)])
async def create(blogpost: Blogpost) -> dict:
    try:
        db["blogs"].update(blogpost)
        return {"message": "success"}
    except Exception as e:
        return {"error": str(e)}
