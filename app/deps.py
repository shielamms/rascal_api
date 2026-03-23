"""Route dependencies such as authorisation check for certain operations."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.db import engine
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
