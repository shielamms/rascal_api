"""DB intiialisation and operations"""
from sqlmodel import Session, SQLModel, create_engine, select

from app.config import settings
from app.models import User, UserCreate
from app.security import hash_password


database_url = settings.DATABASE_URL
engine = create_engine(database_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def init_data() -> None:
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        ).first()
        if not user:
            init_user = UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                user_type=0,  # Admin user
                given_name="Admin",
                last_name="User",
            )
            user = User.model_validate(
                init_user, update={"hashed_password": hash_password(init_user.password)}
            )
            session.add(user)
            session.commit()
            session.refresh(user)