from fastapi import APIRouter, Depends, HTTPException, status

from core.services.user.errors import IntegrityViolationError
from core.logging.logger import logger
from sqlmodel.ext.asyncio.session import AsyncSession
from core.db.session import get_async_session
from core.services.user.service import UserService
from api.schemas.users import GetAllUsersResponse, CreateUserResponse, CreateUserRequest

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session=session)


@router.get("/", response_model=GetAllUsersResponse)
async def get_all_users_handler(user_service: UserService = Depends(get_user_service)) -> GetAllUsersResponse:
    try:
        users = await user_service.get_all_users()
        return GetAllUsersResponse(data=users)
    except Exception as e:
        logger.error(f"error occured : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_handler(
    request: CreateUserRequest, user_service: UserService = Depends(get_user_service)
) -> CreateUserResponse:
    try:
        created_user = await user_service.create_user(user_data=request)
        return CreateUserResponse(data=created_user)
    except IntegrityViolationError as e:
        logger.error(f"db error occured: {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error(f"internal error occured: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
