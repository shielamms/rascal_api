from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.db import engine
from app.config import settings
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        token_json = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ENCODING_ALGORITHM]
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        # pylint: disable=raise-missing-from
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = session.exec(select(User).where(User.email == token_json.get("sub"))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials of user",
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


# Only allow admin users (user_type == 0) to access certain routes like user management
def get_current_active_admin(current_user: CurrentUser) -> User:
    if current_user.user_type != 0:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


CurrentAdminUser = Annotated[User, Depends(get_current_active_admin)]
