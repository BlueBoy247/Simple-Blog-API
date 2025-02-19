from fastapi import FastAPI
from app.routers import router

app = FastAPI()

# include routers
app.include_router(router)

@app.get("/", include_in_schema=False)
async def root() -> dict:
    return {"alive": True}
