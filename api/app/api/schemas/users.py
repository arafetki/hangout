from pydantic import BaseModel

from core.lib.pydantic import CreateUserSchema
from core.db.models.users import User


class GetAllUsersResponse(BaseModel):
    data: list[User]


class CreateUserRequest(CreateUserSchema):
    pass


class CreateUserResponse(BaseModel):
    data: User
