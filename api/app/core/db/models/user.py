from datetime import datetime
from sqlmodel import SQLModel, Field, Column, text
from typing import Optional
from enum import Enum
import sqlalchemy.dialects.postgresql as pg
from core.utils.nanoid import nanoid
from core.utils.helpers import generate_random_username


class UserGender(Enum):
    FEMALE = "female"
    MALE = "male"


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(
        sa_column=Column(name="id", primary_key=True, type_=pg.CHAR(7), default=nanoid),
    )
    email: str = Field(sa_column=Column(name="email", type_=pg.VARCHAR(255), unique=True, nullable=False))
    username: str = Field(
        sa_column=Column(
            name="username", type_=pg.VARCHAR(255), nullable=False, unique=True, default=generate_random_username
        ),
    )
    first_name: str = Field(sa_column=Column(name="first_name", type_=pg.VARCHAR(255), nullable=False))
    last_name: Optional[str] = Field(sa_column=Column(name="last_name", type_=pg.VARCHAR(255), nullable=True))
    gender: UserGender = Field(
        sa_column=Column(
            name="gender",
            type_=pg.ENUM(UserGender, name="user_gender"),
            nullable=False,
        ),
    )
    last_login: Optional[datetime] = Field(
        sa_column=Column(name="last_login", type_=pg.TIMESTAMP(timezone=True), nullable=True)
    )
    created_at: datetime = Field(
        sa_column=Column(
            name="created_at",
            type_=pg.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
