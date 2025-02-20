"""
This module contains the main router, which includes the blog and login routers.
"""

from fastapi import APIRouter
from app.routers import blog, login

router = APIRouter()

router.include_router(blog.router)
router.include_router(login.router)
