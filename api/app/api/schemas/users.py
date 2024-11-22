from pydantic import BaseModel

from app.core.db.models.users import User
from typing import Optional, Literal


class GetAllUsersResponse(BaseModel):
    data: list[User]


class CreateUserRequest(BaseModel):
    email: str
    first_name: str
    last_name: Optional[str]
    gender: Literal["male", "female"]


class CreateUserResponse(BaseModel):
    data: User
