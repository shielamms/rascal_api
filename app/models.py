from datetime import datetime, timezone
import uuid
from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import SQLModel, Field


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# User models
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    status: int = 1
    last_name: str | None = Field(default=None, max_length=255)
    given_name: str | None = Field(default=None, max_length=255)
    user_type: int = 1  # 0: admin, 1: regular user

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    created_at: datetime = Field(
        default_factory=get_datetime_utc, sa_type=DateTime(timezone=True)
    )
    hashed_password: str
    subscription_id: uuid.UUID | None = None

class UserCreate(UserBase):
    # Model for user creation
    password: str = Field(min_length=8, max_length=128)

class UserPublic(UserBase):
    # Model for public user data (e.g. for reading user profiles)
    id: uuid.UUID
    created_at: datetime


# Login models
class LoginRequest(SQLModel):
    email: EmailStr
    password: str

class SessionToken(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Event models
class EventBase(SQLModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None)
    start_time: datetime = Field(sa_type=DateTime(timezone=True))
    end_time: datetime = Field(sa_type=DateTime(timezone=True))
    max_attendees: int | None = None
    status: int = 1  # -1: cancelled, 0: finished, 1: active

class Event(EventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc, sa_type=DateTime(timezone=True)
    )


# Evetn registration models
class EventRegisteration(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc, sa_type=DateTime(timezone=True)
    )
    user_id: uuid.UUID = Field(foreign_key="user.id")
    event_id: uuid.UUID = Field(foreign_key="event.id")
    status: int = 1  # 0: cancelled, 1: active
