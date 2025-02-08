from fastapi import APIRouter
from . import blog, login

router = APIRouter()

router.include_router(blog.router)
router.include_router(login.router)
