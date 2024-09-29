
from services import UserService
from schemas import CreateUser, Token

from typing import Annotated

from fastapi import APIRouter, Response, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status

router = APIRouter(tags=['auth'], prefix='/auth')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends()
):
    username = form_data.username
    password = form_data.password
    tokens = await user_service.login_user(username, password)
    response.set_cookie(key='refresh_token',
                        value=tokens['refresh_token'], httponly=True)
    return Token(
        access_token=tokens['access_token'],
        token_type='bearer'
    )


@router.post('/register', status_code=status.HTTP_200_OK)
async def register(
        form: CreateUser,
        user_service: UserService = Depends()
):
    return await user_service.create_user(form)


@router.post('/update-token', status_code=status.HTTP_200_OK,
             response_model=Token)
async def update_token(
        request: Request,
        user_service: UserService = Depends()
):
    refresh_token = request.cookies.get('refresh_token')
    token = await user_service.update_token(refresh_token)
    return Token(
        access_token=token,
        token_type='bearer'
    )
