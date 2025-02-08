import os
from datetime import datetime, timedelta, timezone
from secrets import token_hex
from typing import Annotated

import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
from dotenv import load_dotenv
from app.database import fake_db as db
from app.schemas import Token, TokenData

SECRET_KEY = token_hex(32)
print(SECRET_KEY)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

load_dotenv()
JWT_ISSUER = os.getenv("JWT_ISSUER")
print(JWT_ISSUER)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(
    prefix="/login",
    tags=["login"],
)

def create_jwt_token(user: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    nbf = datetime.now(timezone.utc)
    to_encode = {
        "email": user,
        "iss": JWT_ISSUER,
        "exp": exp,
        "nbf": nbf,
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    def credentials_exception(detail: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        issuer: str = payload.get("iss")
        if email is None:
            raise credentials_exception("Could not validate credentials")
        if issuer != JWT_ISSUER:
            raise credentials_exception("Invalid token issuer")
        token_data = TokenData(email=email)
    except ExpiredSignatureError as e:
        raise credentials_exception("Token expired") from e
    except InvalidTokenError as e:
        raise credentials_exception("Invalid token") from e

    user = db["users"].get(token_data.email, None)
    if user is None:
        raise credentials_exception("No such user")
    return user

@router.post("")
async def login(email: str, password: str) -> Token:
    hash_pwd = db["users"].get(email)
    if not hash_pwd:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No such user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not pwd_context.verify(password, hash_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_jwt_token(email)
    return Token(access_token=token, token_type="bearer")
