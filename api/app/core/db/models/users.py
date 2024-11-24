from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column
from typing import Optional
import sqlalchemy.dialects.postgresql as pg
from app.core.utils.nanoid import nanoid
from app.core.utils.helpers import generate_random_username
from app.core.utils.enums import UserGender


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(
        sa_column=Column(name="id", primary_key=True, type_=pg.CHAR(7), default=nanoid),
    )
    username: str = Field(
        sa_column=Column(
            name="username",
            type_=pg.VARCHAR(255),
            nullable=False,
            unique=True,
            default=generate_random_username,
            index=True,
        ),
    )
    email: str = Field(sa_column=Column(name="email", type_=pg.VARCHAR(255), unique=True, nullable=False, index=True))
    first_name: str = Field(sa_column=Column(name="first_name", type_=pg.VARCHAR(255), nullable=False))
    last_name: Optional[str] = Field(sa_column=Column(name="last_name", type_=pg.VARCHAR(255), nullable=True))
    gender: UserGender = Field(
        sa_column=Column(name="gender", type_=pg.ENUM(UserGender, name="user_gender"), nullable=False),
    )
    created_at: datetime = Field(
        sa_column=Column(
            name="created_at",
            type_=pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
        ),
    )
