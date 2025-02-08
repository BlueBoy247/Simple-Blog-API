from fastapi import FastAPI
from app.routers import router
from app.routers.login import pwd_context
from app.database import fake_db as db

app = FastAPI()

# include routers
app.include_router(router)

@app.get("/", include_in_schema=False)
async def root():
    return {"alive": True}

# admin, for testing
@app.get("/admin", include_in_schema=False)
async def admin():
    return db

@app.post("/admin/users", include_in_schema=False)
async def admin_users(email: str, password: str):
    if len(email) == 0 or len(password) == 0:
        return {"error": "email or password is empty"}
    db["users"][email] = pwd_context.hash(password)
    return {"message": "success"}
