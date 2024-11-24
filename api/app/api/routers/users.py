from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.db.session import get_async_session
from app.core.services.user.service import UserService
from api.schemas.users import (
    GetAllUsersResponse,
    GetUserResponse,
)
from app.core.utils.helpers import is_valid_nanoid
from app.core.logging.logger import logger
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session=session)


@router.get("/", response_model=GetAllUsersResponse)
async def get_users_handler(
    user_service: UserService = Depends(get_user_service),
    username: Optional[str] = None,
) -> GetAllUsersResponse:
    try:
        users = await user_service.get_users(username=username)
        return GetAllUsersResponse(data=users)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching users."
        )


@router.get("/{user_id}", response_model=GetUserResponse)
async def get_user_handler(user_id: str, user_service: UserService = Depends(get_user_service)) -> GetUserResponse:
    if not is_valid_nanoid(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return GetUserResponse(data=user)
