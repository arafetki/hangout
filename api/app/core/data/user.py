from pydantic import BaseModel
from core.utils.enums import UserGender
from typing import Optional
from datetime import datetime


class CreateUserParams(BaseModel):
    email: str
    first_name: str
    last_name: Optional[str]
    gender: UserGender


class UpdateUserParams(BaseModel):
    username: Optional[str]
    email: Optional[str]
    firt_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[UserGender]
    last_login: Optional[datetime]
