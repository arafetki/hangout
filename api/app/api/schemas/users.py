from pydantic import BaseModel

from app.core.db.models.users import User

class GetAllUsersResponse(BaseModel):
    data: list[User]

class GetUserResponse(BaseModel):
    data: User

