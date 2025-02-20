"""
This module contains the login router, which handles user authentication and JWT generation.
"""

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

def credentials_exception(detail: str) -> HTTPException:
    """
    Raises an HTTPException for 401 Unauthorized with a message detail.

    Args:
        detail (str): The detail message to be included in the response.

    Returns:
        HTTPException: The raised HTTPException.
    """

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

def create_jwt(email: str) -> str:
    """
    Creates a JWT for the given user's email address.

    The token is set to expire in 30 days. The "nbf" claim is set to the current time.

    Args:
        email (str): The email address to encode in the JWT.

    Returns:
        str: The JWT as a string.
    """

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
    """
    Retrieves the user associated with the given JWT token.

    The user is retrieved from the database using the email address encoded in the JWT token.
    If the token is invalid or has expired, an HTTPException is raised.

    Args:
        token (Annotated[str, Depends(oauth2_scheme)]):
            The JWT token to validate and retrieve user data from.
        db (Session): SQLAlchemy session

    Returns:
        dict: The user data as a dictionary.

    Raises:
        HTTPException: If the token is invalid or has expired, or if the user is not found.
    """

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
    """
    Login with email and password.

    Args:
        email (str): Email address to log in with.
        password (str): Password to log in with.

    Returns:
        schemas.Token: The JWT token and its type.

    Raises:
        HTTPException: If the email or password is invalid.
    """

    user = crud.get_user(db, email)
    if not user:
        raise credentials_exception("No such user")
    if not pwd_context.verify(password, user.password):
        raise credentials_exception("Incorrect password")

    token = create_jwt(email)
    return schemas.Token(access_token=token, token_type="bearer")
