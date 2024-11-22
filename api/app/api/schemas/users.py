from pydantic import BaseModel

from app.core.data.user import CreateUserParams
from app.core.db.models.users import User


class GetAllUsersResponse(BaseModel):
    data: list[User]


class CreateUserRequest(CreateUserParams):
    pass


class CreateUserResponse(BaseModel):
    data: User


class GetUserResponse(BaseModel):
    data: User


class DeleteUserResponse(BaseModel):
    detail: str
