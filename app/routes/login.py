""" Routes for user login-related operationsfrom datetime import timedelta."""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.deps import SessionDep
from app.models import SessionToken, User
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/")
def login_user(
    session: SessionDep, login_request: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> SessionToken:
    user = session.query(User).filter(User.email == login_request.username).first()

    if not user:
        verify_password(login_request.password, "DUMMY_HASH")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    verified = verify_password(login_request.password, user.hashed_password)
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data=str(user.email),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return SessionToken(access_token=access_token)

