"""Routes for user-related CRUD operations."""
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.deps import (
    CurrentUser,
    Depends,
    SessionDep,
    get_current_active_admin,
)
from app.models import (
    User,
    UserCreate,
    UserPublic,
    UsersPublic,
)
from app.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", dependencies=[Depends(get_current_active_admin)])
def create_user(new_user: UserCreate, session: SessionDep) -> User:
    # Only admins can create new users
    existing_user = session.exec(
        select(User).where(User.email == new_user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User.model_validate(
        new_user, update={"hashed_password": hash_password(new_user.password)}
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get(
    "/", dependencies=[Depends(get_current_active_admin)], response_model=UsersPublic
)
def read_users(
    session: SessionDep, limit: int = 100, offset: int = 0, include_deactivated=False
) -> list[User]:
    statement = select(User)
    if not include_deactivated:  # Active users only
        statement = statement.where(User.status == 1)
    users = session.exec(statement.offset(offset).limit(limit)).all()
    return UsersPublic(data=users)


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user
