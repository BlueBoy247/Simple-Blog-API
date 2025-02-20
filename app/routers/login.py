import os
from datetime import datetime, timedelta, timezone
from secrets import token_hex
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
from app import crud, schemas
from app.database import get_db

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None or len(SECRET_KEY) < 32:
    SECRET_KEY = token_hex(32)
    with open(".env", "a", encoding="utf-8") as f:
        f.write(f"SECRET_KEY={SECRET_KEY}\n")

JWT_ISSUER = os.getenv("JWT_ISSUER")
if JWT_ISSUER is None or len(JWT_ISSUER) == 0:
    JWT_ISSUER = "fastapi"
    with open(".env", "a", encoding="utf-8") as f:
        f.write(f"JWT_ISSUER={JWT_ISSUER}\n")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(
    prefix="/login",
    tags=["login"],
)

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

def create_jwt(email: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    nbf = datetime.now(timezone.utc)
    to_encode = {
        "email": email,
        "iss": JWT_ISSUER,
        "exp": exp,
        "nbf": nbf,
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
    ) -> dict:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        issuer = payload.get("iss")
        if email is None:
            raise credentials_exception("Could not validate credentials")
        if issuer != JWT_ISSUER:
            raise credentials_exception("Invalid token issuer")
        token_data = schemas.TokenData(email=email)
    except ExpiredSignatureError as e:
        raise credentials_exception("Token expired") from e
    except InvalidTokenError as e:
        raise credentials_exception("Invalid token") from e

    user = crud.get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception("No such user")
    return user

@router.post("")
async def login(email: str, password: str, db: Session = Depends(get_db)) -> schemas.Token:
    user = crud.get_user(db, email)
    if not user:
        raise credentials_exception("No such user")
    if not pwd_context.verify(password, user.password):
        raise credentials_exception("Incorrect password")

    token = create_jwt(email)
    return schemas.Token(access_token=token, token_type="bearer")
