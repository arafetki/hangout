from pydantic import BaseModel, Field
from app.core.utils.enums import UserGender
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

class UserFilterSchema(BaseModel):
    username: Optional[str] = None
    gender: Optional[UserGender] = None
    page_num: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)

    def offset(self) -> int:
        return (self.page_num - 1) * self.page_size