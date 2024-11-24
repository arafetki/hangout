from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.db.models.users import User
from app.core.data.user import CreateUserParams, UpdateUserParams
from typing import Optional
from sqlmodel import select, desc, col
from app.core.services.user.errors import (
    UserCreationError,
    UserNotFoundError,
    UserUpdateError,
    UserDeleteError,
    IntegrityViolationError,
)
from sqlalchemy.exc import IntegrityError


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: CreateUserParams) -> User:
        new_user = User(**user_data.model_dump())
        self.session.add(new_user)

        try:
            await self.session.commit()
            return new_user
        except IntegrityError as e:
            await self.session.rollback()
            if "unique constraint" in str(e.orig):
                raise IntegrityViolationError("A user with this email already exists.")
            raise IntegrityViolationError("A database integrity violation occurred.")

        except Exception as e:
            await self.session.rollback()
            raise UserCreationError(f"An unkown error occurred while creating the user: {e}")

    async def get_users(self,username: Optional[str] = None) -> list[User]:
        stmt = select(User).order_by(desc(User.created_at))
        if username:
            stmt = stmt.where(col(User.username).ilike(f"%{username}%"))
        result = await self.session.exec(stmt)

        return list(result.all())

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.exec(stmt)
        return result.first()

    async def update_user(self, user_id: str, user_data: UpdateUserParams) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
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
            raise UserUpdateError(f"An error occurred while updating the user: {e}")

    async def delete_user(self, user_id: str):
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        await self.session.delete(user)
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise UserDeleteError(f"An error occurred while deleting the user: {e}")
