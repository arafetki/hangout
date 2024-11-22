from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.db.models.users import CreateUserModel, UpdateUserModel, User
from typing import Optional
from sqlmodel import select, desc
from core.services.errors import UserCreationError, UserNotFoundError, UserUpdateError, UserDeleteError


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: CreateUserModel) -> User:
        new_user = User(**user_data.model_dump())
        self.session.add(new_user)

        try:
            await self.session.commit()
            return new_user
        except Exception as e:
            await self.session.rollback()
            raise UserCreationError("An error occurred while creating the user.") from e

    async def get_all_users(self) -> list[User]:
        stmt = select(User).order_by(desc(User.created_at))
        result = await self.session.exec(stmt)

        return list(result.all())

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.exec(stmt)
        return result.first()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.exec(stmt)
        return result.first()

    async def update_user(self, user_id: str, user_data: UpdateUserModel) -> Optional[User]:
        user = await self.get_user(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        for k, v in user_data.model_dump(exclude_unset=True).items():
            if hasattr(user, k):
                setattr(user, k, v)
        try:
            await self.session.commit()
            return user
        except Exception as e:
            await self.session.rollback()
            raise UserUpdateError("An error occurred while updating the user.") from e

    async def delete_user(self, user_id: str):
        user = await self.get_user(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        await self.session.delete(user)
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise UserDeleteError("An error occurred while deleting the user.") from e
