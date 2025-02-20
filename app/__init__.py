"""
This module contains the main FastAPI application.
"""

from fastapi import FastAPI
from app.routers import router

app = FastAPI()

# include routers
app.include_router(router)

@app.get("/", include_in_schema=False)
async def root() -> dict:
    """Root endpoint for health check, returns a simple JSON indicating the service is alive."""

    return {"alive": True}
