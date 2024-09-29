from models import User
from core.utils import get_current_user
from schemas import ShortUser
from services import UserService

from typing import Annotated
from fastapi import APIRouter, Path, Depends
from starlette import status

router = APIRouter(tags=['users'], prefix='/users')


@router.get('/me', status_code=status.HTTP_200_OK,
            summary='Получить текущего пользователя')
async def get_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@router.get('/{user_id}', status_code=status.HTTP_200_OK,
            summary='Получить пользователя по его ID',
            response_model=ShortUser)
async def get_user(
        user_id: Annotated[int, Path(ge=1, description='ID пользователя')],
        user_service: UserService = Depends()
):
    user = await user_service.get_by_id(user_id)
    return ShortUser(
        id=user.id,
        email=user.email,
        fullname=user.fullname,
        joined=user.created_at.date()
    )
